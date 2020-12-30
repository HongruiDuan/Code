#coding=utf-8

from sympy import *

from math import pi,sqrt
#计算基站到设备之间的丢包率
def LossRate_BS(d1, d2):

    distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
    #print d1.position[0], d1.position[1], "to", d2.position[0], d2.position[1], "dis:",distance
    # 计算丢包率
    y = Symbol('y')
    a = 3.0
    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (2.0 / a - 1) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2.0 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
    nk = 1.0 ** (2.0 / a)
    nk = nk * 5.0 / (10.0 ** 8)
    ek = ek * nk
    BSR = exp(-ek)

    PLR = 1 - BSR ** 1024
    return PLR

#计算两个设备之间的丢包率
def LossRate_FDS_RU(d1, d2):

    distance = sqrt((d1.position[0] - d2.position[0]) ** 2 + (d1.position[1] - d2.position[1]) ** 2)
    # 计算丢包率
    y = Symbol('y')
    a = 3.0
    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (2.0 / a - 1) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2.0 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
    nk = 1.0 ** (2.0 / a)
    nk = nk * 5.0 / (10.0 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    # print("比特误码率", (1 - BSR))
    PLR = 1 - BSR ** 1024

    return PLR