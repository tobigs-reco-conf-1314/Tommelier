import os
import sys
import gc
import glob
import joblib
from tqdm import tqdm

import ast
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


def preprocessing(df, str_features, int_features, df_type = 'train'):
    
    feature_names = str_features + int_features

    # feature type 변경
    def setType(df):
        # float -> int을 위한 전처리
        df['rating_average'] = df['rating_average'].apply(lambda x : x * 10)
        df['acidity_y'] = df['acidity_y'].apply(lambda x : x * 10)
        # grapes_id를 embedding 하기 위한.. 모든 grapes_id를 emb하고 싶었으나 너무 어려움..ㅠ
        df['grapes_id'] = df['grapes_id'].apply(lambda x : '[0]' if x == '0' else x)
        df['grapes_id'] = df['grapes_id'].apply(lambda x : ast.literal_eval(x))
        df['grapes_id'] = df['grapes_id'].apply(lambda x : x[0])
         
        for f in str_features:
            if df[f].dtype == float:
                df[f] = df[f].astype(int)

        for f in int_features:
            df[f] = df[f].astype(int)
            
        return df
    
    # 데이터 dict로 변환
    def generateDict(df):
        # str features는 encoding
        train_str_dict = {
        str_feature: [str(val).encode() for val in df[str_feature].values]
        for str_feature in str_features
        }
        # int features는 int
        train_int_dict = {
            int_feature: df[int_feature].values
            for int_feature in int_features
            }

        # label columns이 있다면~
        try:
            train_label_dict = {
                'like' : df['like'].values
            }
            train_str_dict.update(train_label_dict)
        except:
            pass
        try:
            train_label_dict = {
                'rating_per_user' : df['rating_per_user'].values
            }
            train_str_dict.update(train_label_dict)
        except:
            pass
    
        train_str_dict.update(train_int_dict)
        
        return train_str_dict


    df_copy = setType(df)
    input_dict = generateDict(df_copy)

    # tensor
    tensor = tf.data.Dataset.from_tensor_slices(input_dict)
    cached = tensor.shuffle(100_000).batch(8192).cache()
    # unique data 저장
    # train data 일 때, 
    if df_type == 'train':
        vocabularies = {}
    
        for feature_name in tqdm(feature_names):
            vocab = tensor.batch(1_000_000).map(lambda x: x[feature_name])
            vocabularies[feature_name] = np.unique(np.concatenate(list(vocab)))
    
        return cached, vocabularies
      
      # test data 일 때, 
    else:
        return cached


class model(tfrs.Model):
    
    def __init__(self, use_cross_layer, deep_layer_sizes, learning_rate, str_features, int_features, vocabularies, projection_dim = None, metric = 'binary'):
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
    
        if use_cross_layer:
            self._cross_layer = tfrs.layers.dcn.Cross(
                projection_dim = projection_dim,
                kernel_initializer = "glorot_uniform")
        else:
            self._cross_layer = None
    
        self._deep_layers = [tf.keras.layers.Dense(layer_size, activation="relu")
            for layer_size in deep_layer_sizes]
    
        self._logit_layer = tf.keras.layers.Dense(1,
                                                  activation = 'sigmoid'
                                                  )
    
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
        if self._cross_layer is not None:
            x = self._cross_layer(x)
        
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