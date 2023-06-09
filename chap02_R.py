import pandas as pd

df = pd.read_csv(r'C:\ITWILL\pandas\data-analysis-pandas-main\ch_02\data\parsed.csv')
df.info()

# 1. mb 지진규모 유형으로 사용해 일본 진도의 95번째 백분위수를 찾는다.
df['magType']
df['mag']
df['place']
mb = df[(df.magType == 'mb') & (df.parsed_place == 'Japan') ]
mag_95 = mb['mag'].quantile(0.95)
mag_95 # 4.9

# 2. 인도네시아에서 쓰나미가 동반된 지진의 백분율을 구한다.
id = len(df[(df.parsed_place =='Indonesia') & (df.tsunami == 1)]) / len(df[df.parsed_place =='Indonesia']) * 100
id # 0.23129251700680273

df[df.parsed_place == 'Indonesia'].tsunami.value_counts(normalize=True).iloc[1,] # 0.23129251700680273
f"{0.23:.2%}" # 23.00%

# 3. 네바다 지진에 대한 요약 통계를 계산한다.
df[df.parsed_place == 'Nevada'].describe()

# 4. 지진이 불의 고리에 있는 국가나 미국 주에서 발생했는지를 나타내는 열을 추가 한다. 알래스카Aaska, 남극 대륙 Antaratica, Antarctic, 
# 볼리비아 Boliva, 캘리포니아 callornie, 캐나다 Canada, 칠레Chile, 코스타리기Costa Rica, 에콰도르 Eouador, 피지 Fiji, 과테 말라Guatemala,
# 인도네시아 Indonesia. 일본Japan 케르마덱 제도Kermadec Inslands, 멕시코 Mexco (뉴멕시코New MeXiCO를 선택하면 안 된다), 
# 뉴질랜드New zealand, 페루Peru, 필리핀 Philppins, 러시아 Rusia, 타이완Taiwan, 통가Tonga, 워싱턴Washington 을 사용한다.