import pandas as pd
import yfinance as yf
from datetime import datetime

def fetch_prices(input_filename, period="1mo"):
    """
    input_filename: CSV 파일 경로
    period: 데이터를 가져올 기간 (예: "1d", "5d", "1mo", "3mo", "1y", "2y", "5y", "10y", "ytd", "max")
    """
    # 종목 코드 로드
    df_tickers = pd.read_csv(input_filename)

    # 6자리가 되도록 앞에 0 채우기
    df_tickers['Ticker'] = df_tickers['Ticker'].apply(lambda x: str(x).zfill(6))

    # yfinance에서 사용할 수 있는 종목 코드 형식으로 변환
    tickers = [f"{ticker}.KS" if market == "코스피" else f"{ticker}.KQ" for ticker, market in zip(df_tickers['Ticker'], df_tickers['Market'])]

    # 주어진 기간 동안의 가격 데이터 가져오기
    data = {}
    for ticker in tickers:
        try:
            # progress=False를 추가하여 진행상황 출력 비활성화
            stock_data = yf.download(ticker, period=period, progress=False)
            data[ticker] = stock_data['Close']
        except:
            print(f"Error fetching data for {ticker}")

    # 데이터프레임으로 변환
    df_prices = pd.DataFrame(data)

    # CSV 파일로 저장
    output_filename = f"{input_filename.split('.')[0]}_{period}_prices.csv"
    df_prices.to_csv(output_filename)

    print(f"CSV 파일 {output_filename} 저장 완료!")

# 함수 실행 예제
fetch_prices('common_08-18.csv')
