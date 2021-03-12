#coding=utf-8

from math import sqrt



# 基站到FD之间的发送功率之比为 20/0.004 = 5000
# 10 ** -11    800
#
#

path_loss_ratio_BS_RU = -11

# FDS之间的发射功率之比比较小 0.004/0.004 = 1
# 10 ** -6      20
# 10 ** -6.5    40
# 10 ** -7     100
# 10 ** -9     800
path_loss_ratio_FD_RU = - 7.5


# Energy harvest path loss
# 超过100m的范围基本就衰减到0了



D2D_dis_limit = 100 * sqrt(2)

