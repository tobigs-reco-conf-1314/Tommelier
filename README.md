# 투믈리에

투믈리에는 와인 추천 시스템으로, 와잘알(와인을 잘 아는 사람)과 와못알(와인을 잘 모르는 사람)이라는 사용자의 특징을 고려한 추천 시스템입니다.
<br>
투믈리에는 [투빅스 11회 컨퍼런스]()에서 소개되었으며, [발표 자료]()와 [웹 페이지]()를 통해서 더욱 자세한 사항을 확인할 수 있습니다.
<br>
와인 추천을 위해 사용된 데이터는 [vivino](https://www.vivino.com/FR/en/)에서 크롤링을 통해 확보하였습니다.

---------

## 0. 파일구조

```python
투믈리에
├── README.md
├── Preprocessing
│   ├───crawling.py
│   └───preprocessing.py
│   
├── Data
│   ├───
│   ├───
│   ├───
│   ├───
│   
├── Models
│   ├───NMF.py
│   ├───DCN.py
│   └───GCN.py
│   
├── Results
│   ├──NMF_main.ipynb
│   ├──DCN_main.ipynb
│   ├──DeepFM_main.ipynb
│   └──GCN_main.ipynb

```
