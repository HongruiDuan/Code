# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# 构建数据
x_data = [i for i in range(0, 20)]
y_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 2, 0, 0, 0, 7, 9, 7]
y_data2 = [0, 0, 1, 1, 0, 1, 1, 1, 1, 0,
           1, 1, 1, 2, 0, 1, 1, 5, 3, 4]
# 绘图
bar_width = 0.3

plt.bar(x=np.arange(len(x_data)) - bar_width / 2, height=y_data, label='UO',
        color='steelblue', alpha=0.8, width=bar_width)

plt.bar(x=np.arange(len(x_data)) + bar_width / 2, height=y_data2,
        label='MMO', color='indianred', alpha=0.8, width=bar_width)
labelx = range(1, 21)
plt.xticks(x_data, labelx, fontsize=14)

# 设置标题

# 为两条坐标轴设置名称
plt.xlabel("FD No.")
plt.ylabel("FD Selected Frequency")
# 显示图例
plt.legend()
plt.show()