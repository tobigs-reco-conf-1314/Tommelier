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



def DCN(df, str_features, int_features, df_type = 'train'):
    
    feature_names = str_features + int_features

    # feature type 변경
    def setType(df):
        # float -> int을 위한 전처리
        df['rating_average'] = df['rating_average'].apply(lambda x : x * 10)
        df['acidity_y'] = df['acidity_y'].apply(lambda x : x * 10)
        # grapes_id를 embedding 하기 위한.. 모든 grapes_id를 emb하고 싶었으나 너무 어려움..ㅠ
        df['grapes_id'] = df['grapes_id'].apply(lambda x : '[0]' if x == '0' else x)
        df['grapes_id'] = df['grapes_id'].apply(lambda x : ast.literal_eval(x))
        
        if 'user_note_TF' in str_features:

            # user_note 유무와 user_note 길이 feature 생성
            df['user_note_TF'] = df['user_note'].apply(lambda x :  0 if x == '' else 1)
            df['user_note_len'] = df['user_note'].apply(lambda x : len(x))
            
            # 2번째 grapes_id feature 생성
            df['grapes_id2'] = df['grapes_id'].apply(lambda x: x[1] if len(x) > 1 else 0)
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

    
