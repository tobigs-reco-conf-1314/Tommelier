# -*- coding: utf-8 -*-
"""1203_candidate_model_v2_dataset_foodtoken

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BzvXydAKrxY65L5fVBUxfqTw9lW7EHdA
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import gc
from tqdm import tqdm

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
test = '/content/drive/MyDrive/tobigs14_conference/data/v_2/test_all_meta_v2.json'
test_all_meta = pd.read_json(test)

train = '/content/drive/MyDrive/tobigs14_conference/data/v_2/train_all_meta_v2.json'
train_all_meta = pd.read_json(train)

test_all_meta['wine_id'].unique()

RAW_v2 = '/content/drive/MyDrive/tobigs14_conference/data/v_2/RAW_v2_201130.json'
RAW_v2 = pd.read_json(RAW_v2)

RAW = '/content/drive/MyDrive/tobigs14_conference/data/v_2/user_train.json'
RAW = pd.read_json(RAW)

RAW_v2.drop(['index'], axis=1, inplace=True)

df2 = pd.DataFrame(columns=[list(RAW_v2.columns)])
df2

"""### user train set test set 만들기(최신순으로)"""

RAW_v2['userID'].unique()

user_test = pd.DataFrame(RAW_v2[RAW_v2['userID']==19484511].iloc[[0]])
for i in RAW_v2['userID'].unique()[1:]:
    user_test=pd.concat([user_test, pd.DataFrame(RAW_v2[RAW_v2['userID']==i].iloc[[0]])])

user_test

user_test.to_json('user_test.json')
!ls
from google.colab import files
files.download('user_test.json')

user_test.to_csv('user_test.csv')
!ls
from google.colab import files
files.download('user_test.csv')

"""## usertrain"""

user_train = pd.DataFrame(RAW_v2[RAW_v2['userID']==19484511].iloc[1:])
for i in RAW_v2['userID'].unique()[1:]:
    user_train=pd.concat([user_train, pd.DataFrame(RAW_v2[RAW_v2['userID']==i].iloc[1:])])

user_train

user_train.reset_index(inplace=True , drop=True)

user_train.drop(['index'], axis=1, inplace=True)

user_train

user_train.to_csv('user_train.csv')
!ls
from google.colab import files
files.download('user_train.csv')

user_train.to_json('user_train.json')
!ls
from google.colab import files
files.download('user_train.json')

wine_meta = '/content/drive/MyDrive/tobigs14_conference/data/v_2/Wine_Meta_v1_201129.json'
wine_meta = pd.read_json(wine_meta)

wine_meta

"""- 변수 정리
index : raw기준 index <br>
user_note : 리뷰내용 <br>
rating_per_user : 리뷰평점 <br>
vintage_id : 빈티지 id <br>
user_like_count : 다른 사용자의 좋아요 수 <br>
user_id : 유저 ID <br>
wine_id : 와인 Id <br>
wine_name : 와인 이름(년도 포함) <br>
url : 와인 주소 <br>
like : 1=like, 0=dislike <br>
name : 와인 이름 <br>
rating_count : 평점 수 <br>
rating_average : 평점 평균 <br>
rating_distribution : 평점 분포 ({1': 30, '2': 50 ..}) <br>
label_count : 와인 생산 수 <br>
review_count : 리뷰 수 <br>
type_id : 와인 타입 ID (1: 레드와인) <br>
body : 바디 지수 <br>
acidity : 산도 지수 <br>
alcohol : 알코올 지수 <br>
food : 어울리는 음식 리스트<br>
grapes : 포도 리스트 <br>
grapes_id : 포도 ID 리스트 <br>
grapes_count : 포도별 와인 Count <br>
grape_composition : 포도 조합 비중 <br>
rank : 랭크<br>
region_id : 지역 ID <br>
region_name : 지역 이름 <br>
country_code : 지역 코드 <br>
country_most_used_grapes_id : 국가 내 가장 많이 쓴 포도 품종 ID <br>
country_most_used_grapes_name : 국가 내 가장 많이 쓴 포도 품종 이름 <br>
country_most_used_grapes_wines_count : 국가 내 가장 많이 쓴 포도 품종 와인 갯수 <br>
winery_id : 와이너리 ID(양조장) <br> 
winery_name : 와이너리 이름 <br>
winery_ratings_count : 와이너리 평가 수<br>
winery_ratings_average : 와이너리 평가 평균 <br>
winery_labels_count : 와이너리 생산 와인 수<br>
winery_wines_count : 와이너리 생산 와인종류 수 <br>
user_follower_count : 해당 유저의 팔로워 수<br>
user_following_count : 해당 유저의 팔로잉 수<br>
user_rating_count : 해당 유저의 평가 수<br>
user_rating_sum : 해당 유저의 평가 합<br>
reviews_count : 해당 유저의 리뷰 수<br>

# wine_profile 만들기 (wine_id, vintage_id, winenery_id, type_id, body, acidity, alcohol, winery_ratings_count)
winery를 넣은 이유: 같은 양조장에서 만들면 와인이 비슷할 것이고, <br> 와이너리의 평가가 높을 수록 유명한 와인이 많을 수 있기 때문

# wine_test token화 (one_hot_encoding 사용)
"""

train_all_meta['food'][763382]

train_all_meta.head()

train_all_meta['grapes_id'].values

train_all_meta[train_all_meta['vintage_id']==92014915]['food']

train_all_meta['vintage_id'].unique()

len(list(train_all_meta['wine_id'].unique()))

df

wine_meta

food=wine_meta.iloc[:, [1, 11]]

food

# wine_id와 food로 묶기
'''
df=pd.DataFrame(columns=['wine_id', 'food'])
for i in list(wine_meta['wine_id'].unique()):
    df=df.append(wine_meta[RAW_v2['wine_id']==i].iloc[:, [1, 20]])
'''

food

# 특수문자 제거
food['food']=food['food'].map(lambda x: str(x).lstrip('[').rstrip(']'))
food['food'].replace(r'\([^)]*\)', '', regex=True, inplace=True)
food['food'].replace(r',', '|', regex=True, inplace=True)

map(str.strip, my_list)

# 원핫 인코딩
one_hot=pd.Series(food['food']).str.get_dummies()

one_hot

food['food']=food['food'].map(lambda x: str(x).lstrip('[').rstrip(']'))

one_hot.columns

df_1=pd.merge(food, one_hot, left_index=True, right_index=True, how='left')

df_1

import re
document = re.sub(r'[^ ㄱ-ㅣ가-힣A-Za-z]', '', str(list(df_1.columns))) #특수기호 제거, 정규 표현식

col_list=[]
for i in df_1.columns:
    col_list.append(i.lstrip().rstrip().strip("'"))

col_list

df_1.columns=col_list

df_1

df_1=df_1.sort_values('wine_id')

df_1.reset_index(drop=True, inplace=True)

df_1

df_1.to_csv('food_token_one_hot.csv')
files.download('food_token_one_hot.csv')



food_token_one_hot = '/content/drive/MyDrive/tobigs14_conference/data/v_2/food_token_one_hot.csv'
food_token_one_hot_wine = pd.read_csv(food_token_one_hot)

train_all_meta['']==food_token_one_hot_wine['wine_id'].unique()

"""## 의미없는 코드"""

from sklearn.preprocessing import OneHotEncoder

df1=df_1.reset_index()

df_1

X.toarray()

token_food=pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names() )

token_food.drop('and', axis=1)

food_token=pd.concat([df1, token_food], axis=1)

files.download('food_token.json')
files.download('food_token_1.csv')

food_token = '/content/drive/MyDrive/tobigs14_conference/data/v_2/food_token.csv'
food_token_wine = pd.read_csv(food_token)
food_token_wine=food_token_wine.drop(['Unnamed: 0', 'index','vintage_id','and'], axis=1)

# food에 종류별로 라벨링한것 하나로 합치기
food_cols = list(food_token_wine.columns)[2:]
food_encoded = {x: i for i, x in enumerate(food_cols)}

def get_taste(food, tastes):
  def get_all_taste(gs):
    active = [str(food_encoded[taste]) for taste, g in zip(tastes, gs) if g==1]
    if len(active) == 0:
      return '0'
    return ','.join((active))
  food_token_wine['all_food'] = [
      get_all_taste(gs) for gs in zip(*[food_token_wine[taste] for taste in tastes])]
get_taste(food_token_wine, food_cols)
# 출처: https://github.com/revathijay/Python-Notebooks/blob/master/Recommendation/MovieLens_Youtube_Recommendation_Candidate_Generation_Network.ipynb

food_token_wine

"""# user_profile 만들기 (user_id, user_follower count, user_following_count, user_rating_count, user_rating_sum)"""

user_ids = train_all_meta['userID'].unique().tolist()
user2user_encoded = {x: i for i, x in enumerate(user_ids)}
userencoded2user = {i: x for i, x in enumerate(user_ids)}

wine_ids = train_all_meta["wine_id"].unique().tolist()
wine2wine_encoded = {x: i for i, x in enumerate(wine_ids)}
wine_encoded2wine = {i: x for i, x in enumerate(wine_ids)}

train_all_meta_copy = train_all_meta.copy()

train_all_meta_copy['userID'] = train_all_meta["userID"].map(user2user_encoded)
#train_all_meta_copy["wine_id"] = train_all_meta["wine_id"].map(wine2wine_encoded)

train_all_meta_copy

user=(pd.DataFrame(zip(train_all_meta_copy['userID'],
                        train_all_meta_copy['wine_id'],
                        train_all_meta_copy['user_follower_count'],
                        train_all_meta_copy['user_following_count'],
                        train_all_meta_copy['user_rating_count'],
                        train_all_meta_copy['user_rating_sum'],
                        ), columns = ['userID', 'wine_id', 'follower', 'following', 'rating_count', 'rating_sum']))

user

recent_item = user.groupby('userID').agg({
    'wine_id' : [('wine_id', 'unique')]
}).reset_index()

recent_item[['userID', 'wine_id']]

user_data=pd.merge(user, recent_item, how = 'left', on='userID')

user_data.rename(columns = {('wine_id', 'wine_id') : 'wine_tot'}, inplace = True)

user_data

"""# predict label 뽑기 각 user들은 비슷한 와인을 뽑는다는 가정하에 wine_tot에서 random한 와인을 추출"""

import random
random.choice(user_data['wine_tot'][1])

user_data['wine_tot'][0]

user_data['wine_tot'][0]random.choice(user_data['wine_tot'][0])

random.choice(user_data['wine_tot'][0])

user_data

import random
list_predict_label=[]
for idx, val in  enumerate(user_data['wine_tot']):
    #user_data['predict_label'][idx] = random.choice(val)
    list_predict_label.append(random.choice(val))
    user_data['wine_tot'][idx]=np.delete(user_data['wine_tot'][idx], np.where(user_data['wine_tot'][idx]==list_predict_label[idx]))

list_predict_label

user_data.to_csv('user_data.csv')

files.download('user_data.csv')

"""# wine_id 기준으로 wine_profile, food_token, user_profile 통합"""

pd.merge(wine_profile, user_data,  how = 'left', on='wine_id')

user_data



Wine_Meta_final_201208 = '/content/drive/MyDrive/tobigs14_conference/data/v_2/Wine_Meta_final_201208.csv'
Wine_Meta_final = pd.read_csv(Wine_Meta_final_201208)

Wine_Meta_final

Wine_Meta_v1_201129 = '/content/drive/MyDrive/tobigs14_conference/data/v_2/Wine_Meta_v1_201129.json'
Wine_Meta_v1 = pd.read_json(Wine_Meta_v1_201129)

Wine_Meta_v1

len(Wine_Meta_v1['wine_id'].unique())

# wine_world_rank
list_rank=[]
for i in range(len(Wine_Meta_v1['rank'])):
    try:
        list_rank.append(Wine_Meta_v1['rank'][i]['global']['rank'])
    except:
        list_rank.append(float('nan'))

len(list_rank)

rank_wine=pd.DataFrame(list_rank, columns=['world_rank'])

rank_wine[rank_wine['world_rank']==811]

Wine_Meta_final_2=pd.concat([Wine_Meta_final, rank_wine], axis=1)

wine_col=list(Wine_Meta_final_2.columns)

wine_col.insert(2, wine_col[-1])

del wine_col[-1]

Wine_Meta_final_2=Wine_Meta_final_2[wine_col]

for i in np.where(Wine_Meta_final_2['world_rank'].isna()):
    print(i)

Wine_Meta_final_2

Wine_Meta_final_2.to_json('Wine_Meta_final_201210.json')
!ls

Wine_Meta_final_2.to_csv('Wine_Meta_final_201210.csv')
!ls

Wine_Meta_final_2.to_csv('Wine_Meta_final_201210.csv')
!ls
from google.colab import files
files.download('Wine_Meta_final_201210.json')

list_rank