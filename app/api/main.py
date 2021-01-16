from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://192.168.0.9:3000",
    "http://tommelier.ml/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df_wines = pd.read_json('./Meta_with_cluster.json')

MOOD_KOR2IDX = {
    "음식과 함께": 1,
    "가볍게 즐기기 좋은": 2,
    "달콤한 분위기": 3,
    "디저트와 함께": 4,
    "파티 분위기": 5,
    "취하고 싶을 때": 6,
}

FOOD_NAME_KOR2ENG = {
    '닭고기': 'Poultry',  # 4 양계류
    '돼지고기': 'Pork',  # -> 2,4 (바디감에 따라 높으면 4번, 낮으면 2번)
    '소고기': 'Beef',  # -> 2,4 (바디감 1번, 산미  4번) if 바디감도 높고 산미도 높다면?
    '양고기': 'Lamb',  # 4 양
    '연어/참치': 'Rich fish (salmon, tuna etc)',  # 생선 2
    '조개': 'Shellfish',  # 생선 2
    '흰살생선': 'Lean fish',  # 생선 -> 2,4 (바디감에 따라 높으면 4번, 낮으면 2번)
    '매운 음식': 'Spicy food',  # -> 4
    '파스타': 'Pasta',  # -> 2,4 (바디감에 따라 높으면 4번, 낮으면 2번)
    '버섯': 'Mushrooms',  # -> 4
    '채소': 'Vegetarian',  # -> 2
    '식전주': 'Aperitif',  # 식전주 -> 2번 클러스터
    '에피타이저': 'Appetizers and snacks',  # 4번 클러스터
    '단 디저트': 'Sweet desserts',  # 달달한 디저트  -> 4 -> 7번 와인
    '과일 디저트': 'Fruity desserts',  # 과일 디저트 -> 4 -> 7번 와인
    '부드러운 치즈': 'Mild and soft cheese',  # -> 2
    '딱딱한 치즈': 'Mature and hard cheese',  # -> 1
    '블루치즈': 'Blue cheese',  # -> 4
}


class Input(BaseModel):
    mood: str
    food: str
    sweet: int
    tannin: int
    body: int
    acidity: int


@app.post("/reco/")
async def get_recommendation(inputs: Input):
    recommended_wine_ids = get_recommendation(**inputs.dict())
    return {"wine_ids": recommended_wine_ids}


def get_recommendation(mood, food, sweet, tannin, body, acidity, df_wines=df_wines):
    # mood (1~6), food ('Pork', 'Lamb' etc), sweet, tannin, body, acidity
    mood = MOOD_KOR2IDX.get(mood, 1)
    food = FOOD_NAME_KOR2ENG.get(food, 'Pork')

    if mood in [1, 2]:
        if food in ['Poultry', 'Lamb']:
            candidate = df_wines.loc[df_wines.cluster == 1, :]

        elif food in ['Pork', 'Lean fish', 'Pasta']:
            if body > 3:
                candidate = df_wines.loc[df_wines.cluster == 4, :]
            else:
                candidate = df_wines.loc[df_wines.cluster == 2, :]

        elif food == 'Beef':
            if body > acidity:
                candidate = df_wines.loc[df_wines.cluster == 1, :]
            elif body < acidity:
                candidate = df_wines.loc[df_wines.cluster == 4, :]
            else:
                candidate = df_wines.loc[df_wines.cluster.isin([1, 4]), :]

        elif food in ['Rich fish (salmon, tuna etc)', 'Shellfish', 'Vegetarian', 'Aperitif', 'Mild and soft cheese']:
            candidate = df_wines.loc[df_wines.cluster == 2, :]

        elif food in ['Spicy food', 'Mushrooms', 'Appetizers and snacks', 'Blue cheese']:
            candidate = df_wines.loc[df_wines.cluster == 4, :]

        elif food in ['Sweet desserts', 'Fruity desserts']:
            candidate = df_wines.loc[(df_wines.cluster == 4) & (
                df_wines.type_id == 7), :]

        elif food == 'Mature and hard cheese':
            candidate = df_wines.loc[df_wines.cluster == 1, :]

        candidate['taste_score'] = sweet*candidate.sweetness + tannin * \
            candidate.tannin + body*candidate.body + acidity*candidate.acidity
        candidate['taste_score'].fillna(
            candidate.taste_score.mean(), inplace=True)
        candidate.food.fillna({i: [] for i in candidate.index}, inplace=True)
        candidate.taste_score = candidate.taste_score + \
            (candidate.food.map(lambda foods: food in foods).astype(int)) * 10

    else:
        if mood == 3:  # 달콤한 분위기
            if food in ['Beef', 'Lamb', 'Pasta', 'Poultry', 'Pork', 'Lean fish']:
                candidate = df_wines.loc[df_wines.cluster == 3, :]
                candidate = candidate.loc[candidate.food.map(
                    lambda foods: food in foods)]

            else:
                candidate = df_wines.loc[df_wines.cluster == 3, :]

        elif mood == 4:  # 디저트
            if food in 'Sweet desserts':
                candidate = df_wines.loc[(df_wines.cluster == 4) & (
                    df_wines.type_id == 7), :]
                candidate = candidate.loc[candidate.food.map(
                    lambda foods: 'Sweet desserts' in foods)]

            elif food in 'Fruity desserts':
                candidate = df_wines.loc[(df_wines.cluster == 4) & (
                    df_wines.type_id == 7), :]
                candidate = candidate.loc[candidate.food.map(
                    lambda foods: 'Fruity desserts' in foods)]

            else:
                candidate = df_wines.loc[df_wines.cluster == 4, :]

        elif mood == 5:  # 파티용
            candidate = df_wines.loc[(df_wines.cluster == 2) & (
                df_wines.type_id == 3), :]
            food_includes = candidate.food.map(lambda foods: food in foods)
            if food_includes.sum() > 10:
                candidate = candidate.loc[food_includes]

        elif mood == 6:
            if food in ['Beef', 'Pork', 'Lamb', 'Poultry', 'Rich fish (salmon, tuna etc)', 'Shellfish' 'Spicy food', 'Vegetarian', 'Sweet desserts', 'Mild and soft cheese', 'Mature and hard cheese', 'Blue cheese']:
                candidate = df_wines.loc[(df_wines.cluster == 4) & (
                    df_wines.type_id == 24), :]
            else:
                candidate = df_wines.loc[df_wines.type_id == 24, :]
        print(mood)
        candidate['taste_score'] = sweet*candidate.sweetness + tannin * \
            candidate.tannin + body*candidate.body + acidity*candidate.acidity
        candidate['taste_score'].fillna(
            candidate.taste_score.mean(), inplace=True)
        candidate.food.fillna({i: [] for i in candidate.index}, inplace=True)
        candidate.taste_score = candidate.taste_score + \
            candidate.food.map(lambda foods: food in foods).astype(int) * 5

    candidate = candidate.sort_values(['taste_score'], ascending=False)[:30]
    candidate = candidate.sort_values(
        ['rating_average', 'review_count'], ascending=False)

    wine_ids = list(candidate['wine_id'][:10])
    return wine_ids
