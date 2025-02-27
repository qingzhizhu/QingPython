import struct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def read_tdx_day_file(file_path):
    """
    读取通达信.day日线文件
    返回格式: DataFrame[date, open, high, low, close, amount, volume]
    """
    # 定义二进制数据格式（每32字节一条记录）
    data_format = 'iiiiifii'
    data_size = struct.calcsize(data_format)
    
    data_list = []
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(data_size)
            if not chunk:
                break
            # 解包二进制数据
            (date, open_price, high, low, close, 
             amount, vol, _) = struct.unpack(data_format, chunk)
            
            # 价格处理（通达信价格单位：元×1000）
            open_price = open_price / 1000.0
            high = high / 1000.0
            low = low / 1000.0
            close = close / 1000.0
            
            # 日期处理（示例：20230101 → '2023-01-01'）
            date_str = str(date)
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            
            data_list.append([
                formatted_date, open_price, high, low, close, 
                amount, vol  # amount: 成交额（元）, vol: 成交量（手）
            ])
    
    columns = ['date', 'open', 'high', 'low', 'close', 'amount', 'volume']
    df = pd.DataFrame(data_list, columns=columns)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# 示例：读取浦发银行（sh600000.day）
tdx_data_dir = r'/Users/kevin/info/GP/tdx/vipdoc/sh/lday'  # 需修改为你的通达信目录
file_path = os.path.join(tdx_data_dir, 'sh600000.day')
df = read_tdx_day_file(file_path)

# 查看数据
print(df.head())

# ----------------------
# 扩展功能：计算技术指标
# ----------------------
# 计算5日均线和20日均线
df['MA5'] = df['close'].rolling(window=5).mean()
df['MA20'] = df['close'].rolling(window=20).mean()

# 计算波动率（20日收益率标准差）
df['returns'] = df['close'].pct_change()
df['volatility_20'] = df['returns'].rolling(20).std() * np.sqrt(252)

# ----------------------
# 可视化
# ----------------------
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Close Price')
plt.plot(df['MA5'], label='5-Day MA')
plt.plot(df['MA20'], label='20-Day MA')
plt.title('TDX Stock Data Analysis')
plt.legend()
plt.show()
