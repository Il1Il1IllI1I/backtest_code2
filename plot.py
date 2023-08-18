import pandas as pd
import matplotlib.pyplot as plt

def plot_portfolio_performance(prices_csv='recent_30_days_prices.csv', tickers_csv='minervini_buy_tickers_20230816_092603.csv'):
    # Matplotlib 한글 폰트 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows용
    plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 문제 해결

    # 가격 데이터 CSV 파일 로드
    df_prices = pd.read_csv(prices_csv, index_col=0)
    df_tickers = pd.read_csv(tickers_csv)
    df_tickers['Ticker'] = df_tickers['Ticker'].apply(lambda x: str(x).zfill(6))
    ticker_to_name = dict(zip(df_tickers['Ticker'], df_tickers['Name']))

    # 각 종목의 30일간의 수익률 계산
    returns = (df_prices.iloc[-1] - df_prices.iloc[0]) / df_prices.iloc[0] * 100

    # 전체 포트폴리오의 수익률 계산
    portfolio_return = returns.mean()

    # 결과 시각화
    plt.figure(figsize=(15, 10))
    ax = returns.sort_values().plot(kind='bar', color='blue', alpha=0.7)
    plt.axhline(y=portfolio_return, color='r', linestyle='-')
    plt.title('각 종목의 최근 30일 수익률 및 전체 포트폴리오 수익률')
    plt.ylabel('수익률 (%)')
    plt.xlabel('종목 코드')
    plt.xticks([])

    # 각 막대 위에 종목 이름 표시 (세로로 눕힘)
    for idx, rect in enumerate(ax.patches):
        ticker = returns.sort_values().index[idx]
        ticker_name = ticker_to_name.get(ticker.split('.')[0], 'Unknown')
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.5*height, ticker_name, ha='center', va='bottom', fontsize=10, color='white', rotation=90)

    plt.legend(['전체 포트폴리오 수익률', '종목별 수익률'])
    plt.tight_layout()
    plt.show()

# 사용 예시
plot_portfolio_performance('common_08-18_1mo_prices.csv', 'common_08-18.csv')
