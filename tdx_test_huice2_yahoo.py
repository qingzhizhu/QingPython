import pandas as pd
import backtrader as bt

# 假设 data 是从 pytdx 获取的数据
data = pd.DataFrame({
    'datetime': pd.date_range(start='2020-01-01', periods=100),
    'open': range(100, 200),
    'high': range(110, 210),
    'low': range(90, 190),
    'close': range(100, 200),
    'volume': range(1000, 1100)
})

# 确保 datetime 是索引
data.set_index('datetime', inplace=True)

# 自定义 PandasData 类
class PytdxData(bt.feeds.PandasData):
    params = (
        ('datetime', None),     # 使用 DataFrame 索引作为时间
        ('open', 'open'),       # 开盘价列名
        ('high', 'high'),       # 最高价列名
        ('low', 'low'),         # 最低价列名
        ('close', 'close'),     # 收盘价列名
        ('volume', 'volume'),   # 成交量列名
        ('openinterest', -1),   # 无持仓量字段
    )

# 创建 Backtrader 数据源
datafeed = PytdxData(dataname=data)

# 初始化回测引擎
cerebro = bt.Cerebro()
cerebro.adddata(datafeed)

# 添加策略
cerebro.addstrategy(bt.strategies.SMA_CrossOver)

# 运行回测
cerebro.run()
cerebro.plot()