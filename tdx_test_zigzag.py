import pandas as pd
from pytdx.hq import TdxHq_API

# ----------------------
# 1. 使用 pytdx 获取日线数据
# ----------------------
def get_pytdx_daily_data(symbol, market):
    """
    获取A股日线数据
    :param symbol: 股票代码（如 '600000'）
    :param market: 市场代码（0=深圳，1=上海）
    :return: DataFrame[datetime, open, high, low, close, volume]
    """
    api = TdxHq_API()
    try:
        # 连接通达信服务器
        if not api.connect('124.71.187.122', 7709):
            raise ConnectionError("无法连接服务器")
        
        # 获取日线数据（最多 800 条）
        data = api.to_df(api.get_security_bars(
            category=9,          # 9=日线数据
            market=market,       # 0=深圳，1=上海
            code=symbol,         # 股票代码
            start=0,             # 起始位置
            count=800            # 获取数量（最大 800）
        ))
        
        # 数据清洗
        data = data[['datetime', 'open', 'high', 'low', 'close', 'vol']]
        data.rename(columns={'vol': 'volume'}, inplace=True)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data.set_index('datetime', inplace=True)
        return data
    
    finally:
        api.disconnect()

# ----------------------
# 2. 实现改进的 ZigZag 指标
# ----------------------
def calculate_zigzag(data, deviation=0.01, depth=10, use_percentage=True):
    """
    计算改进的 ZigZag 指标
    :param data: DataFrame，包含价格数据（需有 high 和 low 列）
    :param deviation: 价格变化的最小百分比或绝对值阈值
    :param depth: 回溯的 K 线数量
    :param use_percentage: 是否使用百分比阈值
    :return: DataFrame，包含 ZigZag 高点和低点
    """
    highs = data['high']
    lows = data['low']
    zigzag = pd.Series(index=data.index, dtype=float)
    last_pivot = None
    trend = None  # 1=上升趋势，-1=下降趋势

    for i in range(depth, len(data)):
        window_highs = highs.iloc[i-depth:i]
        window_lows = lows.iloc[i-depth:i]
        
        # 当前窗口的最高点和最低点
        current_high = window_highs.max()
        current_low = window_lows.min()
        
        # 确定趋势反转
        if last_pivot is None:
            last_pivot = current_high if highs.iloc[i] == current_high else current_low
            trend = 1 if highs.iloc[i] == current_high else -1
        else:
            if trend == 1:
                if use_percentage:
                    condition = lows.iloc[i] < last_pivot * (1 - deviation)
                else:
                    condition = lows.iloc[i] < last_pivot - deviation
                if condition:
                    zigzag.iloc[i] = last_pivot
                    last_pivot = current_low
                    trend = -1
            else:
                if use_percentage:
                    condition = highs.iloc[i] > last_pivot * (1 + deviation)
                else:
                    condition = highs.iloc[i] > last_pivot + deviation
                if condition:
                    zigzag.iloc[i] = last_pivot
                    last_pivot = current_high
                    trend = 1

    # 填充最后一个点
    if trend == 1:
        zigzag.iloc[-1] = highs.iloc[-1]
    else:
        zigzag.iloc[-1] = lows.iloc[-1]

    return zigzag

def zigzag(prices, reversal_percentage):
    zigzag = pd.Series(index=data.index, dtype=float)
    last_extreme = None
    last_extreme_value = None

    for i in range(len(prices)):
        current_price = prices[i]

        if last_extreme is None:
            last_extreme = i
            last_extreme_value = current_price
            zigzag.iloc[i] = current_price #((i, current_price))
            continue

        difference = (current_price - last_extreme_value) / last_extreme_value * 100

        if -(difference) >= reversal_percentage:
#            zigzag.append((i, current_price))
            zigzag.iloc[i] = current_price
            last_extreme = i
            last_extreme_value = current_price
	
	
    return zigzag
    
# ----------------------
# 3. 主程序
# ----------------------
if __name__ == '__main__':
    # 获取日线数据
    symbol = '159828'  # 浦发银行（沪市代码）
    market = 0         # 1=上海市场
    data = get_pytdx_daily_data(symbol, market)
    print(data.head())
    
    # 计算 ZigZag 指标
    deviation = 0.05  # 1% 的价格变化阈值
    depth = 12        # 回溯 10 根 K 线
    use_percentage = True  # 使用百分比阈值
    #zigzag = calculate_zigzag(data, deviation=deviation, depth=depth, use_percentage=use_percentage)
    
    
    zigzag_points = zigzag(data['close'].values, reversal_percentage=5)
	#zigzag_df = pd.DataFrame(zigzag_points, columns=['Index', 'Zigzag Price']).set_index('Index')
    
    # 将 ZigZag 指标添加到数据中
    data['zigzag'] = zigzag_points
    
    # 输出结果
    print(data[['high', 'low', 'zigzag']].dropna())
    #print(data.tail())
    
    # 可视化
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.plot(data['close'], label='Close Price', alpha=0.5)
    plt.scatter(data.index, data['zigzag'], color='red', label='ZigZag Points', marker='o')
    plt.title(f'ZigZag Indicator for {symbol} (日线)')
    plt.legend()
    plt.show()