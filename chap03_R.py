import pandas as pd

# 1.각 주식 csv파일들을 하나의 파일로 결합하고 FANNG 데이터를 이후 연습 문제에 사용할 수 있도록 faang DataFrame으로 저장한다.

# a) 각 csv 파일을 읽는다.
fb = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\fb.csv')
aapl = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\aapl.csv')
amzn = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\amzn.csv')
nflx = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\nflx.csv')
goog = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\goog.csv')

# b) 각 DataFrame에 티커 기호를 나타내는 ticker(예: 애플은 AAPL이다) 열을 추가한다. 연습 문제의 경우의 파일 이름이 티커가 된다.
fb['ticker'] = 'FB'
aapl['ticker'] = 'AAPL'
amzn['ticker'] = 'AMZN'
nflx['ticker'] = 'NFLX'
goog['ticker'] = 'GOOG'

# c) 각 DataFrame을 하나의 DataFrame에 추가한다.
faang = pd.concat([fb,aapl,amzn,nflx,goog])

# d) 결과를 faang.csv 파일로 저장한다.
faang.to_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\faang.csv', index=False)


# 2. faang에서 유형 변환을 사용해 data 열의 값을 datetimes 형식으로, volume 열의 값을 정수형으로 변환한다. 
# 그런 다음 date와 ticker를 기준으로 정렬한다.

faang.dtypes
'''
date     object
volume   float64
'''
faang['date'] = pd.to_datetime(faang['date'])
faang['volume'] = faang['volume'].astype('int')
faang.dtypes

faang = faang.sort_values(by=['date','ticker'])

# 3. faang의 volume 열에서 가장 낮은 값 7개를 찾는다.
volume7 = faang.sort_values(by='volume')[:7]
volume7_2 = faang.nsmallest(7,'volume')
'''
126 2018-07-03  1135.819946  1100.020020  1135.819946  1102.890015  679000   GOOG
226 2018-11-23  1037.589966  1022.398987  1030.000000  1023.880005  691500   GOOG
99  2018-05-24  1080.469971  1066.150024  1079.000000  1079.239990  766800   GOOG
130 2018-07-10  1159.589966  1149.589966  1156.979980  1152.839966  798400   GOOG
152 2018-08-09  1255.541992  1246.010010  1249.900024  1249.099976  848600   GOOG
159 2018-08-20  1211.000000  1194.625977  1205.020020  1207.770020  870800   GOOG
161 2018-08-22  1211.839966  1199.000000  1200.000000  1207.329956  887400   GOOG
'''

# 4. 이제 데이터는 긴 형태와 넓은 형태의 중간에 있다. melt()를 사용해 완전히 긴 형태로 바꾼다.
# 힌트 : date와 ticker는 ID 변수다(이 값들은 각 행을 고유하게 식별 할 수 있다.)
# open, high, low, close, volume 열이 분리되지 않도록 나머지 부분도 멜팅해야 한다.

melted_faang = faang.melt(
    id_vars=['ticker', 'date'], 
    value_vars=['open', 'high', 'low', 'close', 'volume']
)

# 6. 2020년 1월 1일부터 2020년 9월 18일 까지의 코로나19 확진자 수 데이터가 포함된 데이터를 사용하여 데이터를 정제하고 피보팅해 넓은 형태로 만든다.

# a) covid19_cases.csv 파일을 읽는다.
covid19 = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_03\exercises\covid19_cases.csv')

# b) dateRep 열의 데이터와 pd.to_datetime() 함수를 사용해 date열을 만든다.
covid19.dtypes
covid19['date']=pd.to_datetime(covid19['dateRep'],format='%d/%m/%Y')



# c) date 열을 인덱스로 설정하고 인덱스를 기준으로 정렬한다.
covid19.head()
covid19.index = covid19['date']

# d) united_states_of_America와 United_Kingdom의 모든 항목을 각각 USA와 UK로 바꾼다. 
# 힌트: replace() 메서드를 Dataframe 전체에 대해 실행한다.
covid19['countriesAndTerritories'] = covid19['countriesAndTerritories'].replace('United_States_of_America','USA')
covid19['countriesAndTerritories'] = covid19['countriesAndTerritories'].replace('United_Kingdom','UK')
covid19['countriesAndTerritories'][:40]

# e) countriesAndTerritories 열을 사용해 정제한 COVID-19 신규 확진자 수 데이터를
# 아르헨티나Agentina, 브라질Biazal, 중국china, 콜롬비아colombia, 인도Inida, 이탈리아Italy, 멕시코Mexco, 페루Penv,
# 러시아RuSSia, 스페인Spain, 터키Turkey, 영국UK, 미국USA으로 필터링한다.

covid19_f = covid19[covid19['countriesAndTerritories'] == ('Argentina'|'Brazil'|'China'|'Colombia'|'Inida'|'Italy'|'Mexico'|'Peru'|'Russia'|'Turkey'|'UK'|'USA')]


# c('Argentina'|'Brazil'|'China'|'Colombia','Inida','Italy','Mexico','Peru','Russia', 'Turkey','UK','USA')]
# f) 날짜가 인덱스되고 국가명을 열로 하고, 값은 (cases 열에) 신규 확진자 수가 되도 록 데이터를 피보팅한다. NaN은 0으로 채워야 한다.