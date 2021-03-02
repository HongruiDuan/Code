#coding=utf-8

from sympy import *

from math import pi,sqrt
import matplotlib.pyplot as plt
#计算基站到设备之间的丢包率


# TODO:基站广播信道和FD传输信道采用不同的参数进行模拟
# def LossRate_BS(d1, d2):
#
#     distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
#     #print d1.position[0], d1.position[1], "to", d2.position[0], d2.position[1], "dis:",distance
#     # 计算丢包率
#     y = Symbol('y')
#     a = 1.5
#     f1 = y ** (2.0 / a - 1) * exp(-y)
#     f2 = y ** (2.0 / a - 1) * exp(-y)
#     I1 = integrate(f1, (y, 0, oo))
#     I2 = integrate(f2, (y, 0, oo))
#     Ca = (2.0 * pi / a) * I1 * I2
#     ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
#     nk = 1.0 ** (2.0 / a)
#     nk = nk * 5.0 / (10.0 ** 8)
#     ek = ek * nk
#     BSR = exp(-ek)
#
#     PLR = 1 - BSR ** 1024
#     return PLR

#计算两个设备之间的丢包率
# def LossRate_FDS_RU(d1, d2):
#
#     distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
#     # 计算丢包率
#     y = Symbol('y')
#     a = 3.0
#     f1 = y ** (2.0 / a - 1) * exp(-y)
#     f2 = y ** (2.0 / a - 1) * exp(-y)
#     I1 = integrate(f1, (y, 0, oo))
#     I2 = integrate(f2, (y, 0, oo))
#     Ca = (2.0 * pi / a) * I1 * I2
#     ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
#     nk = 1.0 ** (2.0 / a)
#     nk = nk * 5.0 * 10.0 ** -8
#     ek = ek * nk
#     BSR = exp(-ek)
#     # print("比特误码率", (1 - BSR))
#     PLR = 1 - BSR ** 1024
#
#     return PLR

def LossRate_BS(d1, d2):
    distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
    #print d1.position[0], d1.position[1], "to", d2.position[0], d2.position[1], "dis:",distance
    # 计算丢包率
    y = Symbol('y')
    #信道衰减因子
    a = 4.0
    #SINR阈值
    v_c = 3.0

    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (- 2.0 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (v_c ** (2.0 / a))
    P_s = 20 # 20w
    P_r = 0.004 #4mw
    # P_r = 0.0004 #4mw
    gamma = (P_s / P_r) ** (2.0 / a)
    #单位范围内的FD密度  -11的单边覆盖范围大概在500， -12的单边覆盖范围大概在1000左右

    lambda_c = 10 ** (-12)

    #这些参数是如何确定的，以后工作交接的时候，完全搞清楚别人的代码是很困难的，总是会有小细节是不知道的
    sigma = gamma * lambda_c
    ek = ek * sigma
    BSR = exp(-ek)
    PLR = 1 - BSR ** 1024
    return PLR
def LossRate_FDS_RU(d1, d2):
    distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
    #print d1.position[0], d1.position[1], "to", d2.position[0], d2.position[1], "dis:",distance
    # 计算丢包率
    y = Symbol('y')
    #信道衰减因子
    a = 4.0
    #SINR阈值
    v_c = 3.0

    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (- 2.0 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (v_c ** (2.0 / a))
    P_s = 0.004 # 20w
    P_r = 0.004 #4mw
    # P_r = 0.0004 #4mw
    gamma = (P_s / P_r) ** (2.0 / a)
    #单位范围内的FD密度  -11的单边覆盖范围大概在500， -12的单边覆盖范围大概在1000左右

    lambda_c = 10 ** (-12)

    #这些参数是如何确定的，以后工作交接的时候，完全搞清楚别人的代码是很困难的，总是会有小细节是不知道的
    sigma = gamma * lambda_c
    ek = ek * sigma
    BSR = exp(-ek)
    PLR = 1 - BSR ** 1024
    return PLR

def LossRate_test_BS(d):

    distance = d
    #print d1.position[0], d1.position[1], "to", d2.position[0], d2.position[1], "dis:",distance
    # 计算丢包率
    y = Symbol('y')
    #信道衰减因子
    a = 4.0
    #SINR阈值
    v_c = 3.0

    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (- 2.0 / a) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (v_c ** (2.0 / a))
    P_s = 20 # 20w
    P_r = 20 #4mw
    # P_r = 0.0004 #4mw
    gamma = (P_s / P_r) ** (2.0 / a)
    #单位范围内的FD密度  -11的单边覆盖范围大概在500， -12的单边覆盖范围大概在1000左右
    #TODO:为什么影响覆盖范围的主要因素是设备密度？
    lambda_c = 10 ** (-12)

    #这些参数是如何确定的，以后工作交接的时候，完全搞清楚别人的代码是很困难的，总是会有小细节是不知道的
    sigma = gamma * lambda_c
    ek = ek * sigma
    BSR = exp(-ek)
    PLR = 1 - BSR ** 1024
    return PLR

if __name__ == '__main__':

    loss = []
    # 丢包率和距离的关系
    for i in range(1,1001):
        loss.append(LossRate_test_BS(i))
    x = [i for i in range(1,1001)]
    plt.figure()
    plt.plot(x,loss)
    plt.show()




