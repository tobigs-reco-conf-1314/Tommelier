# Tommelier

![투믈리에](https://user-images.githubusercontent.com/48677363/104844095-73f9d100-5911-11eb-8589-bf1eb1ea9df6.jpg)


투믈리에는 와인 추천 시스템으로, 와잘알(와인을 잘 아는 사람)과 와못알(와인을 잘 모르는 사람)이라는 사용자의 특징을 고려한 추천 시스템입니다.
<br>
투믈리에는 [투빅스 11회 컨퍼런스](https://www.youtube.com/watch?v=YZIZwbRkfSA&t=13s)에서 소개되었으며, [발표 자료](https://drive.google.com/file/d/1ULj_U7iKPP_M-ubLHMTgSmxigNSJdmvY/view)와 [웹 페이지](http://tommelier.ml/)를 통해서 더욱 자세한 사항을 확인할 수 있습니다.
<br>
와인 추천을 위해 사용된 데이터는 [vivino](https://www.vivino.com/FR/en/)에서 크롤링을 통해 수집하였습니다.



## 1. Data

프로젝트에서 대표적으로 다룬 데이터는 user meta, item meta, user-item rating 데이터입니다.
<br>
자세한 명세는 [구글 스프레드 시트](https://docs.google.com/spreadsheets/d/1Myp9Oe9B3fByzJjSmSNaqxhyCgYKLTSYc0NgZUHcxUw/edit?usp=sharing)에서 확인 가능합니다.


## 2. Model

  - **Neural Matrix Factorization** - [Neural Collaboratice Filtering](https://arxiv.org/pdf/1708.05031.pdf), 2017, Xiangnan He
  
    - 조상연
    
  - **Deep Factorization Machine** - [DeepFM: A Factorization-Machine based Neural Network for CTR Prediction](https://arxiv.org/pdf/1703.04247.pdf), 2017, Huifeng Guo)
  
    - 장혜림
    - 정세영
    
  - **Deep & Cross Network** - [DCN V2: Improved Deep & Cross Network and Practical Lessons
for Web-scale Learning to Rank Systems](https://arxiv.org/pdf/2008.13535.pdf)(2020, Ruoxi Wang)
  
    - [오진석](https://github.com/tobigs-reco-conf-1314/Tommelier/blob/main/Results/DCN_main.jinseok.ipynb)
    - [박준영](https://github.com/tobigs-reco-conf-1314/Tommelier/blob/main/Results/DCN_main_junyoung.ipynb)
    
  - **Graph Convolutional Network** - [Graph Convolutional Neural Networks for Web-Scale
Recommender Systems](https://arxiv.org/pdf/1806.01973.pdf)(2018, Ying, R)
  
    - 신윤종


## 3. Results

<img width="700" alt="result1" src="https://user-images.githubusercontent.com/48677363/104843792-d4880e80-590f-11eb-860e-828d720cd0f9.png">
<img width="700" alt="result2" src="https://user-images.githubusercontent.com/48677363/104844084-5f1d3d80-5911-11eb-8479-2254bac96e80.png">

## 4. Web Demo

> [웹 데모](http://tommelier.ml/)를 통해 초심자도 간단한 설문만 하면 와인을 추천받을 수 있습니다.


|`Demo Screenshot`|
|--|
|<img src="https://user-images.githubusercontent.com/18041103/104782948-6be24a00-57c8-11eb-8ea9-2095d948411b.png" width=500 />|


## 5. Contributors

- 조상연
- 이지용
- 오진석
- 박준영
- 장혜림
- 정세영
- 신윤종
---------

## Structure

```python
투믈리에
├── README.md
├── Preprocess
│   ├───crawling.py
│   └───preprocess.py
│   
├── Models
│   ├───NeuralMF.py
│   ├───DCN.py
│   ├───DeepFM.py
│   └───GCN
│       ├──
│       └──
│   
├── Results
│   ├──NMF_main.ipynb
│   ├──DCN_main_jinseok.ipynb
│   ├──DCN_main_junyoung.ipynb
│   ├──DeepFM_main.ipynb
│   ├──DeepFM_main.ipynb
│   └──GCN_main.ipynb
│

```



