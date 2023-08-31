import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
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
    return output_filename

def plot_portfolio_performance(prices_csv, tickers_csv):
    """
    포트폴리오 성과를 시각화하는 함수
    """
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False

    df_prices = pd.read_csv(prices_csv, index_col=0)
    df_tickers = pd.read_csv(tickers_csv)
    df_tickers['Ticker'] = df_tickers['Ticker'].apply(lambda x: str(x).zfill(6))
    ticker_to_name = dict(zip(df_tickers['Ticker'], df_tickers['Name']))

    returns = (df_prices.iloc[-1] - df_prices.iloc[0]) / df_prices.iloc[0] * 100
    portfolio_return = returns.mean()

    start_date, end_date = df_prices.index[[0, -1]]
    start_date, end_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%m-%d"), datetime.strptime(end_date, "%Y-%m-%d").strftime("%m-%d")
    
    plt.figure(figsize=(15, 10))
    ax = returns.sort_values().plot(kind='bar', color='cornflowerblue', alpha=0.8)
    plt.axhline(0, color='gray', linestyle='--')
    plt.axhline(portfolio_return, color='r', linestyle='-')
    plt.title(f'각 종목의 최근 {len(df_prices)}일 수익률 및 전체 포트폴리오 수익률\n({start_date} - {end_date})', fontsize=16)
    plt.ylabel('수익률 (%)')
    plt.xlabel('종목 코드')
    plt.xticks([])

    for idx, rect in enumerate(ax.patches):
        ticker = returns.sort_values().index[idx]
        name = ticker_to_name.get(ticker.split('.')[0], 'Unknown')
        ax.text(rect.get_x() + rect.get_width()/2., rect.get_height() + 0.5, f"{name}\n({rect.get_height():.2f}%)", ha='center', fontsize=10)

    plt.legend(['0% 수준', f'전체 포트폴리오 수익률 ({portfolio_return:.2f}%)'], fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 함수 실행
prices_csv = fetch_prices('TurtleMinervini_08-31.csv', period='10d')
plot_portfolio_performance(prices_csv, 'TurtleMinervini_08-31.csv')