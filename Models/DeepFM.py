"""
have to install deepctr package

pip install deepctr
"""

import pandas as pd
import numpy as np
from deepctr.models import DeepFM
from deepctr.feature_column import SparseFeat, DenseFeat, get_feature_names
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import tensorflow as tf
from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score, roc_auc_score


def list_to_str(feature):
    feature_str = []
    for i in range(len(feature)):
        if feature[i]:feature_str.append(' '.join(feature[i])
        else:feature_str.append(' ')

    return feature_str


def id_to_int(feature):
    feature = feature.fillna(0)
    feature = feature.astype(int)
    return feature


def preprocess(X_train, X_test, sparse_features, dense_features, list_features, id_features):

'''
    sparse_features : categorical features including both of list_features and id_features like food, userID
    dense_features : continuous features like rating_count
'''
    
    for feature in list_features:
        X_train[feature] = pd.Series(list_to_str(X_train[feature]), name=feature)
        X_test[feature] = pd.Series(list_to_str(X_test[feature]), name=feature)

    for feature in id_features:
        X_train[feature] = id_to_int(X_train[feature])
        X_test[feature] = id_to_int(X_test[feature])


    # parameters
    EMBEDDING_DIM = 32

    for feat in sparse_features:
        lbe = LabelEncoder()
        all = pd.concat([X_train[feat], X_test[feat]], axis=0).drop_duplicates()
        lbe = lbe.fit(all)
        X_train[feat] = lbe.transform(X_train[feat])
        X_test[feat] = lbe.transform(X_test[feat])


    mms = MinMaxScaler(feature_range=(0, 1))
    X_train[dense_features] = mms.fit_transform(X_train[dense_features])
    X_test[dense_features] = mms.transform(X_test[dense_features])

    fixlen_feature_columns = [SparseFeat(feat, vocabulary_size=pd.concat([X_train[feat], X_test[feat]], axis=0).drop_duplicates().nunique(),embedding_dim=EMBEDDING_DIM)
                               for i,feat in enumerate(sparse_features)] + [DenseFeat(feat, 1,) for feat in dense_features]

    dnn_feature_columns = fixlen_feature_columns
    linear_feature_columns = fixlen_feature_columns

    feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

    X_train.fillna(X_train.mean(), inplace=True)
    X_test.fillna(X_test.mean(), inplace=True)

    train_model_input = {name:X_train[name] for name in feature_names}
    test_model_input = {name:X_test[name] for name in feature_names}


    return linear_feature_columns, dnn_feature_columns, train_model_input, test_model_input



def model_train(y_train, y_test):
    # parameters
    BATCH_SIZE = 256
    EPOCHS = 500
    DROPOUT_RATE = 0.25
    early_stopping = EarlyStopping(monitor='accuracy', verbose=1, patience=10)

    linear_feature_columns, dnn_feature_columns, train_model_input, test_model_input = preprocess(X_train, X_test, sparse_features, dense_features, list_features, id_features)

    model = DeepFM(linear_feature_columns, dnn_feature_columns, task='binary', dnn_dropout=DROPOUT_RATE, dnn_use_bn=True)
    model.compile("adam", "binary_crossentropy",metrics=['accuracy'])

    history = model.fit(train_model_input, y_train.values,
                        batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=2, validation_split=0.2, callbacks=[early_stopping])
    y_pred = model.predict(test_model_input, batch_size=BATCH_SIZE)

    print("test AUC", round(roc_auc_score(y_test.values, y_pred), 4))
    print("test Auccuracy", round(accuracy_score(y_test.values, y_pred.round()), 4))

    return model, y_pred



