# -*- coding:utf-8 -*-
from numpy import random
import math
from mininet.log import info
import json
# from mn_wifi import propagationModels
# from random import gauss

def energy(sta, ap, time):
    staPosition = sta.params['position'][0:2]
    num = str(sta)[1]
    apPosition = ap.params['position'][0:2]
    distance = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)
    info('distance : %.2fm\n' % distance)
    txpower = float(ap.params['txpower'][0]) #根据基站的发射功率计算能量收集
    info('txpower: %.3fdbm\n' % txpower)
    transmitPower = 10 ** (txpower / 10) / 1000
    info('transmitPower: %fW\n' % transmitPower)
    alpha = 2.0
    t, receiveEnergy = 0, 0
    interval = 0.0001
    while t <= time:
        h = random.normal(0, 1)
        receivePower = transmitPower * (distance ** (-alpha)) * (h ** 2)
        receiveEnergy += receivePower * interval
        t += interval
    info('after %ds receive energy : %fJ\n' % (time, receiveEnergy))
    pow = float(receiveEnergy)
    filename = "/home/shlled/mininet-project-duan/Stackelberg/NCLog/UE%c.json" % num
    # print filename
    with open(filename,'r+') as f:
        buffer = f.readlines()
        lenth = len(buffer)            
        data = json.loads(buffer[-1])
        data["POWER"] += pow
        json.dump(data,f)
        f.write("\n")

    
    