import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Mac용)
plt.rcParams['font.family'] = 'AppleGothic'
# Windows용
# plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')  # ggplot 스타일 사용

def show_stock_analysis(stock1, stock2, periods):
    stock1_info = yf.Ticker(stock1).info
    stock2_info = yf.Ticker(stock2).info
    stock1_name = stock1_info.get('longName', stock1)
    stock2_name = stock2_info.get('longName', stock2)
    
    stock1_data = yf.download(stock1)['Adj Close']
    stock2_data = yf.download(stock2)['Adj Close']
    
    data = pd.DataFrame({stock1: stock1_data, stock2: stock2_data}).dropna()
    
    n = len(periods)
    fig, axs = plt.subplots(n, 2, figsize=(14, 7 * n), gridspec_kw={'width_ratios': [3, 1]})
    
    # Make sure axs is always a list of lists
    if n == 1:
        axs = [axs]
        
    for ax_row, (start_date, end_date) in zip(axs, periods):
        sub_data = data[start_date:end_date]
        
        if sub_data.empty:
            print(f"No data available between {start_date} and {end_date}. Skipping this period.")
            continue
        
        # Calculate returns
        stock1_return = ((sub_data[stock1].iloc[-1] / sub_data[stock1].iloc[0]) - 1) * 100
        stock2_return = ((sub_data[stock2].iloc[-1] / sub_data[stock2].iloc[0]) - 1) * 100

        # Calculate volatility
        stock1_volatility = sub_data[stock1].pct_change().std() * (252 ** 0.5) * 100  # Annualized
        stock2_volatility = sub_data[stock2].pct_change().std() * (252 ** 0.5) * 100  # Annualized
        
        ax1, ax3 = ax_row  # ax1 for prices, ax3 for volatility

        ax2 = ax1.twinx()  # Create another y-axis on the same x-axis
        
        ax1.plot(sub_data.index, sub_data[stock1], 'g-', label=f"{stock1_name} ({stock1})")
        ax2.plot(sub_data.index, sub_data[stock2], 'b-', label=f"{stock2_name} ({stock2})")

        ax1.set_xlabel('날짜')
        ax1.set_ylabel(f'{stock1_name} 주가', color='g')
        ax2.set_ylabel(f'{stock2_name} 주가', color='b')

        title = f'{stock1_name}와 {stock2_name}의 주가 차트 ({start_date} ~ {end_date})\n'
        title += f'상관계수: {sub_data.corr().iloc[0, 1]:.2f} / {stock1_name} 변동성: {stock1_volatility:.2f}% / {stock2_name} 변동성: {stock2_volatility:.2f}%'

        ax1.set_title(title)
        
        ax1.text(0.01, 0.95, f"{stock1_name} 수익률: {stock1_return:.2f}%", transform=ax1.transAxes, color='g')
        ax2.text(0.01, 0.85, f"{stock2_name} 수익률: {stock2_return:.2f}%", transform=ax2.transAxes, color='b')
        
        ax1.grid(True)
        ax2.grid(True)
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper center')

        # Plot volatility
        ax3.bar([0, 1], [stock1_volatility, stock2_volatility], tick_label=[stock1_name, stock2_name], color=['g', 'b'])
        ax3.set_ylabel('변동성 (%)')

    plt.tight_layout()
    plt.show()

# 사용 예시
periods = [
    ('2021-06-10', '2023-08-29'),  # 아이폰 15 출시 전
]

show_stock_analysis('USDKRW=X', '069500.KS', periods)
