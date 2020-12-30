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
    P_t = 8000
    G_T = 2
    G_R = 2
    c = 300000000.0
    lamda = c/900000000.0
    L = 0.8
    P_R = P_t *G_T*G_R*(lamda**2)/(L*(4*math.pi*d)**2)
    power = P_R * time
    return power

if __name__ == '__main__':
    BS0 = BS(0,0,0)
    FD1 = FD("FD1",50,0)
    y = []
    for i in range(30,50):
        fd_i = FD("x",i,0)
        y.append( energy(BS0, fd_i, 1) )

    x = [i for i in range(30,50) ]

    plt.xlabel("Distance/m")
    plt.ylabel("EH Power/J")
    plt.plot(x,y)
    plt.show()
