# 투믈리에

투믈리에는 와인 추천 시스템으로, 와잘알(와인을 잘 아는 사람)과 와못알(와인을 잘 모르는 사람)이라는 사용자의 특징을 고려한 추천 시스템입니다.
<br>
투믈리에는 [투빅스 11회 컨퍼런스]()에서 소개되었으며, [발표 자료]()와 [웹 페이지]()를 통해서 더욱 자세한 사항을 확인할 수 있습니다.
<br>
와인 추천을 위해 사용된 데이터는 [vivino](https://www.vivino.com/FR/en/)에서 크롤링을 통해 확보하였습니다.

---------

## 0. 저장소 구조

```python
투믈리에
├── README.md
├── Preprocess
│   ├───crawling.py
│   └───preprocess.py
│   
├── Data
│   ├───train.json
│   ├───test.json
│   └───item.csv
│   
├── Models
│   ├───NeuralMF.py
│   ├───DCN.py
│   └───GCN.py
│   
├── Results
│   ├──NMF_main.ipynb
│   ├──DCN_main.ipynb
│   ├──DeepFM_main.ipynb
│   └──GCN_main.ipynb
│
├── Params
│   ├───NeuralMF
│   │    └───
│   ├───DCN
│   │    ├──vocabularies.json
│   │    └──DCN_weights.tf
│   ├───DeepFM
│   │    ├──
│   │    └──
```

## 1. 데이터

어쩌구저쩌구
비비노 어쩌구
어쩌구

## 2. 모델

  - [Neural MF](https://arxiv.org/pdf/1708.05031.pdf)
  - [DeepFM]()
  - [DCN](https://arxiv.org/pdf/2008.13535.pdf)
  - [GCN]()


## 3. 결과

|Model|Hyper Params|Epochs|Roc|Acc|담당자|
|-----|--------|---|---|---|---|
|DCN|Cross(2) + Deep(512, 256, 128, 64)|1000(78)|0.9582|0.93|오진석|
|DCN|Cross(1) + Deep(256, 128, 64)|1000(276)|0.9528|0.92|오진석|
|DCN|Cross(1) + Deep(192, 192)|1000(161)|0.9520|0.92|오진석|
|   |     |     |     |     |     |
|   |     |     |     |     |     |
|   |     |     |     |     |     |


## 4. 웹



## 5. Contributors

