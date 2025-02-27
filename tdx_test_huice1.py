import pandas as pd
import backtrader as bt
from pytdx.hq import TdxHq_API

# ----------------------
# 1. 使用 pytdx 获取 A 股数据
# ----------------------
def get_pytdx_data(symbol, market):
    """
    获取A股日线数据
    :param symbol: 股票代码（如 '600000'）
    :param market: 市场代码（0=深圳，1=上海）
    :return: DataFrame[datetime, open, high, low, close, volume]
    """
    api = TdxHq_API()
    try:
        # 连接通达信服务器
        # 查ip：https://www.cnblogs.com/BeyondTechnology/p/18456471
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
# 2. 适配 Backtrader 数据格式
# ----------------------
class PytdxData(bt.feeds.PandasData):
    """
    自定义数据适配类，将 pytdx 数据转换为 Backtrader 格式
    """
    params = (
        ('datetime', None),     # 使用 DataFrame 索引作为时间
        ('open', 'open'),       # 开盘价列名
        ('high', 'high'),       # 最高价列名
        ('low', 'low'),         # 最低价列名
        ('close', 'close'),     # 收盘价列名
        ('volume', 'volume'),   # 成交量列名
        ('openinterest', -1),   # 无持仓量字段
    )

# ----------------------
# 3. 定义回测策略（均线交叉策略）
# ----------------------
class SMAStrategy(bt.Strategy):
    params = (
        ('fast', 5),    # 快速均线周期
        ('slow', 20),   # 慢速均线周期
    )

    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=self.params.fast)
        self.sma_slow = bt.indicators.SMA(period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()  # 金叉买入
        else:
            if self.crossover < 0:
                self.sell()  # 死叉卖出

# ----------------------
# 4. 主程序
# ----------------------
if __name__ == '__main__':
    # 获取数据
    symbol = '600000'  # 浦发银行（沪市代码）
    market = 1         # 1=上海市场
    data = get_pytdx_data(symbol, market)
    
    # 创建 Backtrader 数据源
    datafeed = PytdxData(dataname=data)
    
    # 初始化回测引擎
    cerebro = bt.Cerebro()
    
    # 添加数据
    cerebro.adddata(datafeed)
    
    # 添加策略
    cerebro.addstrategy(SMAStrategy)
    
    # 设置初始资金和手续费
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)  # 0.1% 手续费
    
    # 运行回测
    print('初始资金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('最终资金: %.2f' % cerebro.broker.getvalue())
    
    # 绘制图表
    cerebro.plot()