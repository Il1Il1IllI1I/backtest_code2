import pandas as pd
import numpy as np
import FinanceDataReader as fdr
import datetime

def backtest_strategy(ticker):
    """주식 종목 코드를 입력 받아 모든 조건이 충족되면 True를 반환하는 함수"""
    
    # 데이터 가져오기
    data = fdr.DataReader(ticker, start="2022-08-01")
    
    # 이동평균 계산
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA150'] = data['Close'].rolling(window=150).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    # 조건 설정
    conditions = [
        (data['Close'] > data['MA150']) & (data['Close'] > data['MA200']),
        data['MA150'] > data['MA200'],
        data['MA200'] > data['MA200'].shift(21),
        (data['MA50'] > data['MA150']) & (data['MA50'] > data['MA200']),
        data['Close'] > data['MA50'],
        data['Close'] > (data['Low'].rolling(window=252).min() * 1.3),
        data['Close'] >= (data['High'].rolling(window=252).max() * 0.75),
        100 - (100 / (1 + (data['Close'].diff().where(lambda x: x > 0, 0).rolling(window=14).mean() /
                        -data['Close'].diff().where(lambda x: x < 0, 0).rolling(window=14).mean()))) >= 70
    ]
    
       # 최신 데이터에 대한 조건들만 추출
    latest_conditions = [cond.iloc[-1] for cond in conditions]
    return all(latest_conditions)

# 모든 코스피, 코스닥 종목 정보 가져오기
all_stocks = pd.concat([fdr.StockListing('KOSPI'), fdr.StockListing('KOSDAQ')]).set_index('Code')

# True인 종목만 저장하기 위한 리스트
true_tickers = []

# 백테스트 시작 시간 기록
start_time = datetime.datetime.now()

# 각 종목별로 백테스트 실행
for ticker in all_stocks.index:
    print(f"{ticker} - {all_stocks.loc[ticker, 'Name']} 테스트 중...")
    if backtest_strategy(ticker):
        true_tickers.append({'Ticker': ticker, 'Name': all_stocks.loc[ticker, 'Name']})

# 백테스트 종료 시간 기록
end_time = datetime.datetime.now()

# 결과 DataFrame 생성
df = pd.DataFrame(true_tickers)

# 시가총액, 변동률, 시장 정보 추가
df['MarketCap'] = df['Ticker'].apply(lambda x: all_stocks.loc[x, 'Marcap'])
df['Market'] = df['Ticker'].apply(lambda x: all_stocks.loc[x, 'Market'])

# 시가총액으로 내림차순 정렬
df = df.sort_values(by='MarketCap', ascending=False)

# 시가총액 값을 보기 좋게 변경
df['MarketCap'] = (df['MarketCap'] / 10**8).round().astype(int).astype(str) + '억'
df['Market'] = df['Market'].replace({'KOSPI': '코스피', 'KOSDAQ': '코스닥', 'KOSDAQ GLOBAL': '코스닥'})

# 현재 날짜와 시간을 가져와서 문자열로 변환
current_date_str = datetime.datetime.now().strftime('%m-%d')
filename = f"minervini_{current_date_str}.csv"

# 결과 저장
df.to_csv(filename, index=False)

# 백테스트에 걸린 시간 출력
print(f"백테스트에 걸린 시간: {end_time - start_time}")
