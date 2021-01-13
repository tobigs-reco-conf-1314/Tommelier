import os
import sys
import gc
import glob
import joblib
from tqdm import tqdm

import numpy as np
import pandas as pd

import keras
import tensorflow as tf
import tensorflow_recommenders as tfrs

from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Lambda, Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import LambdaCallback, EarlyStopping, Callback
from tensorflow.keras.utils import plot_model

from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
import tensorflow_datasets as tfds


class model(tfrs.Model):
    
    def __init__(self, cross_layer_sizes, deep_layer_sizes, learning_rate, str_features, int_features, vocabularies, projection_dim = None, metric = 'binary'):
        super().__init__()
    
        self.embedding_dimension = 64
    
        self._all_features = str_features + int_features
        self._embeddings = {}
    
        # Compute embeddings for string features.
        for feature_name in str_features:
            vocabulary = vocabularies[feature_name]
            self._embeddings[feature_name] = tf.keras.Sequential(
                [tf.keras.layers.experimental.preprocessing.StringLookup(
                    vocabulary=vocabulary, mask_token=None),
                    tf.keras.layers.Embedding(len(vocabulary) + 1,
                    self.embedding_dimension)
                                             ])
          
    
        # Compute embeddings for int features.
        for feature_name in int_features:
            vocabulary = vocabularies[feature_name]
            self._embeddings[feature_name] = tf.keras.Sequential(
                [tf.keras.layers.experimental.preprocessing.IntegerLookup(
                    vocabulary=vocabulary, mask_value=None),
                    tf.keras.layers.Embedding(len(vocabulary) + 1,
                    self.embedding_dimension)
                                         ])
    
#         if use_cross_layer:
#             self._cross_layer = tfrs.layers.dcn.Cross(
#                 projection_dim = projection_dim,
#                 kernel_initializer = "glorot_uniform")
#         else:
#             self._cross_layer = None
        
        # Cross layer
        if cross_layer_sizes:
            self._cross_layer = [tfrs.layers.dcn.Cross(
                projection_dim = projection_dim,
                kernel_initializer = "glorot_uniform") for _ in range(cross_layer_sizes)]
        else:
            self._cross_layer = None
            
        # Deep layer
        self._deep_layers = [tf.keras.layers.Dense(layer_size, activation="relu")
            for layer_size in deep_layer_sizes]
        
        # Output layer
        self._logit_layer = tf.keras.layers.Dense(1,
                                                  activation = 'sigmoid'
                                                  )
        # Metric
        if metric == 'binary':
            self.task = tfrs.tasks.Ranking(
            loss = tf.keras.losses.BinaryCrossentropy(),
            metrics=[
                    tf.keras.metrics.BinaryAccuracy(
                        name='binary_accuracy', dtype = None, threshold = 0.5)
                    ])
                    
        elif metric == 'reg':
            self.task = tfrs.tasks.Ranking(
                loss=tf.keras.losses.MeanSquaredError(),
                metrics=[
                    tf.keras.metrics.RootMeanSquaredError("RMSE")
                    ])
        else:
            print('metric ERROR!')
            sys.exit(1)
    
    def call(self, features):
        # Concatenate embeddings
        embeddings = []
        for feature_name in self._all_features:
            embedding_fn = self._embeddings[feature_name]
            embeddings.append(embedding_fn(features[feature_name]))
    
        x = tf.concat(embeddings, axis=1)
    
        # Build Cross Network
#         if self._cross_layer is not None:
#             x = self._cross_layer(x)
        for cross_layer in self._cross_layer:
            x = cross_layer(x)
        
        # Build Deep Network
        for deep_layer in self._deep_layers:
            x = deep_layer(x)
    
        return self._logit_layer(x)
    
    def compute_loss(self, features, training=False, metric = 'binary'):
        if metric == 'binary':
            labels = features.pop("like")
        elif metric == 'reg':
            labels = features.pop("rating_per_user")
        scores = self(features)
    
        return self.task(
            labels=labels,
            predictions=scores,
            )

def getResult(model, cached_test, metric = 'binary'):
    
    cached_test_numpy = tfds.as_numpy(cached_test)
    y_true = [item['like'] for item in cached_test_numpy]
    y_true = np.concatenate(y_true)

    y_pred = model.predict(cached_test).flatten()

    if metric == 'binary':
        y_pred_class = [1 if pred > 0.5 else 0 for pred in y_pred]

    print(f"ROC: {roc_auc_score(y_true, y_pred)}")
    print(classification_report(y_true, y_pred_class))


def recommendation(userID, model, item, str_features, int_features):
    item_copy = item.copy()
    item_copy['userID'] = id
    item_copy['like'] = 0
    
    cached = preprocessing(item_copy, str_features, int_features, df_type = 'test')
    pred = model.predict(cached)
    pred = pd.DataFrame(pred).sort_values(0, ascending = False).reset_index()
    pred.columns = ['wine_id', 'prob']
    pred['wine_id'] = item_copy['wine_id'].values
    
    return pred