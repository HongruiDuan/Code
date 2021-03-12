#coding=utf-8

import math
from BaseStation import BS
from FogDevice import FD
import random
import matplotlib.pyplot as plt
#计算单位时间内收集到的能量的函数

def energy(sta, ap, time):
    staPosition = sta.position
    apPosition = ap.position
    d = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)

    # Energy harvest 的发射功率
    # P_t = 8000
    P_t = 2000 # 2kw

    G_T = 2
    G_R = 2
    # c = 300000000.0 #
    c = 3 * 10 ** (8)
    lambda_h = c / (9 * 10 ** (8)) # 波长
    lambda_h = c / 900000000.0
    L = 0.8
    P_R = P_t * G_T * G_R *(lambda_h**2)/(L*(4 * math.pi * d)**2)
    P_R = 4 * 10 ** (-4)
    #这里采用RF transmitter的时候先统一设置为定值 60uw
    power = P_R * time
    return power

if __name__ == '__main__':
    BS0 = BS([0, 0])
    FD1 = FD("FD1",[50,0])
    y = []
    for i in range(10,500):
        fd_i = FD("x", [0,i])
        y.append(energy(BS0, fd_i, 1))

    x = [i for i in range(10,500)]

    plt.xlabel("Distance/m")
    plt.ylabel("EH Power/J")
    plt.plot(x, y)
    plt.show()
