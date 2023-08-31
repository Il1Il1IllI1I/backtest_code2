import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_portfolio_performance(prices_csv, tickers_csv):
    # 한글 폰트 설정 (Mac용)
    plt.rcParams['font.family'] = 'AppleGothic'
    # Windows용
    # plt.rcParams['font.family'] = 'Malgun Gothic'  

    plt.rcParams['axes.unicode_minus'] = False

    # CSV 파일에서 가격과 티커 데이터 읽기
    df_prices = pd.read_csv(prices_csv, index_col=0)
    df_tickers = pd.read_csv(tickers_csv)
    df_tickers['Ticker'] = df_tickers['Ticker'].apply(lambda x: str(x).zfill(6))
    ticker_to_name = dict(zip(df_tickers['Ticker'], df_tickers['Name']))

    # 수익률 계산
    returns = (df_prices.iloc[-1] - df_prices.iloc[0]) / df_prices.iloc[0] * 100
    portfolio_return = returns.mean()

    # 시작일과 종료일 추출
    start_date, end_date = df_prices.index[[0, -1]]
    start_date, end_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%m-%d"), datetime.strptime(end_date, "%Y-%m-%d").strftime("%m-%d")
    
    # 그래프 그리기
    plt.figure(figsize=(15, 10))
    ax = returns.sort_values().plot(kind='bar', color='cornflowerblue', alpha=0.8)
    plt.axhline(0, color='gray', linestyle='--')
    plt.axhline(portfolio_return, color='r', linestyle='-')
    plt.title(f'각 종목의 최근 {len(df_prices)}일 수익률 및 전체 포트폴리오 수익률\n({start_date} - {end_date})', fontsize=16)
    plt.ylabel('수익률 (%)')
    plt.xlabel('종목 코드')
    plt.xticks([])

    # 종목명과 수익률 표시
    for idx, rect in enumerate(ax.patches):
        ticker = returns.sort_values().index[idx]
        name = ticker_to_name.get(ticker.split('.')[0], 'Unknown')
        ax.text(rect.get_x() + rect.get_width()/2., rect.get_height() + 0.5, f"{name}\n({rect.get_height():.2f}%)", ha='center', fontsize=10)

    plt.legend(['0% 수준', f'전체 포트폴리오 수익률 ({portfolio_return:.2f}%)'], fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 예시 사용법
plot_portfolio_performance('common_tickers_10d_prices.csv', 'common_tickers.csv')
