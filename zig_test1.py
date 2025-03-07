import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 生成模拟的价格数据
np.random.seed(42)
time = pd.date_range('2024-01-01', periods=100)
price = np.cumsum(np.random.randn(100)) + 100  # 随机波动
data = pd.DataFrame({'Price': price}, index=time)




def zigzag(prices, reversal_percentage):
    zigzag = []
    last_extreme = None
    last_extreme_value = None

    for i in range(len(prices)):
        current_price = prices[i]

        if last_extreme is None:
            last_extreme = i
            last_extreme_value = current_price
            zigzag.append((i, current_price))
            continue

        difference = (current_price - last_extreme_value) / last_extreme_value * 100

        if abs(difference) >= reversal_percentage:
            zigzag.append((i, current_price))
            last_extreme = i
            last_extreme_value = current_price

    return zigzag
    
zigzag_points = zigzag(data['Price'].values, reversal_percentage=5)
zigzag_df = pd.DataFrame(zigzag_points, columns=['Index', 'Zigzag Price']).set_index('Index')

# 可视化结果
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Price'], label='Price', color='blue', alpha=0.5)
plt.scatter(zigzag_df.index, zigzag_df['Zigzag Price'], color='red', marker='o', label='Zigzag Points')
plt.title('Zigzag Function Visualization')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
#plt.grid()
plt.show()    