import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import struct

# ----------------------
# 1. 解析权息数据文件
# ----------------------
def parse_gpcw_file(gpcw_path, target_code):
    """
    解析权息文件（gpcw.txt），返回复权因子计算表
    """
    columns = ['code', 'name', 'ex_date', 'dividend', 'send_share', 'allot_share', 'allot_price', 'base_share']
    df = pd.read_csv(gpcw_path, sep=',', header=None, names=columns, dtype={'ex_date': str})
    
    # 筛选目标股票的权息记录
    df = df[df['code'] == target_code]
    
    # 转换为日期格式
    df['ex_date'] = pd.to_datetime(df['ex_date'], format='%Y%m%d')
    
    # 计算复权因子（前复权）
    df['factor'] = 1.0
    for i in range(len(df)):  # 从前向后计算
        dividend = df.iloc[i]['dividend']
        send_ratio = df.iloc[i]['send_share'] / 10.0  # 送股比例（例如10送5股，比例为0.5）
        allot_ratio = df.iloc[i]['allot_share'] / 10.0  # 配股比例
        allot_price = df.iloc[i]['allot_price']
        
        # 复权因子计算公式
        adjust_factor = (1 + send_ratio + allot_ratio) * (1 - dividend / (df.iloc[i]['base_share'] / 1e4))
        df.loc[df.index[i], 'factor'] = adjust_factor
    
    # 累积复权因子
    df['cum_factor'] = df['factor'].cumprod()
    return df

# ----------------------
# 2. 应用前复权调整
# ----------------------
def apply_forward_adjustment(stock_data, df_gpcw):
    """
    应用前复权调整到日线数据
    """
    # 合并权息日期和复权因子
    df_merged = pd.merge_asof(
        stock_data.sort_index(),
        df_gpcw.sort_values('ex_date'),
        left_index=True,
        right_on='ex_date',
        direction='backward'
    )
    
    # 填充未复权日期的因子为1
    df_merged['cum_factor'].fillna(1.0, inplace=True)
    
    # 调整价格和成交量
    df_merged['close_adj'] = df_merged['close'] / df_merged['cum_factor']
    df_merged['open_adj'] = df_merged['open'] / df_merged['cum_factor']
    df_merged['high_adj'] = df_merged['high'] / df_merged['cum_factor']
    df_merged['low_adj'] = df_merged['low'] / df_merged['cum_factor']
    df_merged['volume_adj'] = df_merged['volume'] * df_merged['cum_factor']
    
    return df_merged[['close_adj', 'open_adj', 'high_adj', 'low_adj', 'volume_adj']]

# ----------------------
# 3. 读取通达信日线数据
# ----------------------
def read_tdx_day_file(file_path):
    """
    读取通达信.day日线文件
    返回格式: DataFrame[date, open, high, low, close, amount, volume]
    """
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

# ----------------------
# 4. 主程序
# ----------------------
if __name__ == "__main__":
    # 文件路径
    tdx_data_dir = r'/Users/kevin/info/GP/tdx/vipdoc/sh/lday'  # 通达信日线数据目录
    gpcw_path = r'/Users/kevin/info/GP/tdx/vipdoc/cw/gpcw.txt'  # 权息文件路径
    target_code = 600000  # 目标股票代码（示例：浦发银行）
    day_file = os.path.join(tdx_data_dir, f'sh{target_code}.day')  # 日线文件路径

    # 读取日线数据
    stock_data = read_tdx_day_file(day_file)

    # 解析权息数据
    df_gpcw = parse_gpcw_file(gpcw_path, target_code)

    # 应用前复权
    adjusted_data = apply_forward_adjustment(stock_data, df_gpcw)

    # 合并原始数据和复权数据
    result = pd.concat([stock_data, adjusted_data], axis=1)

    # 保存结果
    result.to_csv(f'sh{target_code}_forward_adjusted.csv')

    # 可视化对比
    plt.figure(figsize=(12, 6))
    plt.plot(result['close'], label='原始价格', alpha=0.5)
    plt.plot(result['close_adj'], label='前复权价格', linestyle='--')
    plt.title(f'股票 {target_code} 前复权价格对比')
    plt.legend()
    plt.show()
