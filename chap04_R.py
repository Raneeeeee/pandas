import pandas as pd

# 1. earthquakes.csv 파일에서 mb 진도 유형(magnitude type)의 진도가 4.9 이상인 일본의 모든 지진을 선택한다.
earthquakes = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_04\exercises\earthquakes.csv')
earthquakes.dtypes
over_49 = earthquakes[(earthquakes['mag']>=4.9) & (earthquakes['parsed_place']=='Japan') & (earthquakes['magType']=='mb')]

# 2.  ml 측정 방법의 모든 진도 값에 대한 구간(예를 들어 첫 번째 구간은 (0,1], 두번째는(1,2], 세번째는(2,3])을 만들고 각 구간의 빈도수를 계산한다.
'''
one = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=0) & (earthquakes['mag']<0)]
two = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=1) & (earthquakes['mag']<2)]
three = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=2) & (earthquakes['mag']<3)]
four = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=3) & (earthquakes['mag']<4)]
five = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=4) & (earthquakes['mag']<5)]
six = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=5) & (earthquakes['mag']<6)]
seven = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=6) & (earthquakes['mag']<7)]
'''

bins = np.arange(0, 10)
bins_label = [str(x) + "이상" + str(x + 1) + "미만" for x in bins[:-1]]
earthquakes['level'] = pd.cut(earthquakes['mag'], bins, right=False, labels=bins_label)
result = earthquakes[earthquakes['magType'] == 'ml']
a = result['level'].value_counts()
a.sort_index()


import numpy as np

earthquakes.query("magType == 'ml'").assign(
    mag_bin=lambda x: pd.cut(x.mag, np.arange(0, 10))
).mag_bin.value_counts()  

# 두개 왜 다를까...ㅠ -> 엑셀파일이 다른듯? 실제 데이터 필터 해보니 내가 쓴 정답이 맞네용~~

# 3. faang.csv 파일에서 티커(ticker)로 그룹을 만들고 월별 빈도수 재표본추출한다. 다음과 같이 집계한다.
# a) 시가 평균 b) 고가의 최대값 c) 저가의 최소값 d) 종가 평균 e) 거래량 합

faang = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_04\exercises\faang.csv')
faang.dtypes
faang['date2'] = pd.to_datetime(faang['date'])
faang.index = faang['date2'] # resample 사용하려면 index가 datetime이어야함.
# faang['month'] = faang['date2'].dt.month
faang.groupby('ticker').resample('M').agg(
    {
        'open': np.mean,
        'high': np.max,
        'low': np.min,
        'close': np.mean,
        'volume': np.sum
    }
)
faang.groupby(by='month')

# 4. 지진 데이터에서 tsunami 열과 magType 열의 교차표를 만든다. 교차표에서는 빈도수가 아니라 각 조합에서 관측된 최대 진도가 표시되도록 한다. 
# 열에서는 진도 유형 (magnitude type) 값이 와야한다.
cross = pd.crosstab(earthquakes.tsunami,earthquakes.magType, values=earthquakes.mag, aggfunc=max)

# 5. FAANG 데이터의 티커로 OHLC의 60일 이동집계를 만든다. 연습 문제 3번과 같은 집계를 한다.
# a) 시가 평균 b) 고가의 최대값 c) 저가의 최소값 d) 종가 평균 e) 거래량 합
faang.groupby(faang['ticker']).mean()
a = faang.groupby('ticker').rolling('60D').agg(
        {
        'open' : np.mean,
        'high' : np.max,
        'low' : np.min,
        'close' : np.mean,
        'volume' : np.sum
        }
    )
print(a)

# 6. 주가를 비교하는 FAANG 데이터의 피봇 테이블을 만든다. 행에는 티커가 오도록하고 OHLC의 평균과 거래량 데이터를 표시한다.

# 7. apply()를 사용해 아마존 데이터의 2018년 4분기 (Q4) 각 숫자열의 Z-점수를 계산한다.

#
