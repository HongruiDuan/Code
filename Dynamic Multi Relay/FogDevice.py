#coding=utf-8
import random

from Action import  Action
from LossRate import LossRate_BS
class FD:
  def __init__(self, fdId, position):
    self.fdId = fdId
    self.position = position
    #choice是指的设备编号，setchoice表明的是RU的哪个集合
    self.coalition = None
    self.setchoice = 0
    self.energy = 0

    #雾设备的电池容量最大为3000mA,仿真中一致用的焦耳
    #最大能量为这么多但是并不是所有的能量都用于发送信息


    self.power = random.uniform(0.005, 0.0020)
    #self.power = 0.0020
    #雾设备的发射功率4mw
    self.pow = 0.004
    #雾设备的发送速率大小为100 k/s
    self.rate = 100
    #还需要记录基站到自己的丢包率，来计算自己最多丢失的数据包
    self.BS_FD_lossrate = 0.0

    self.relaynum = 0

    #先是每10轮比较一下utility和expect 再来调整一下自己的选择
    self.round = 0  # round是指每个FD在当前联盟中运行的轮数
    self.total = 0 # total是指每个FD在当前联盟中累积的效用 加的是实际的
    self.utility = 0 # utility的含义暂时没有想好
    self.expect = 0 # expect是指每个FD在加入联盟时的期望效用 表示的是期望的

    self.cumulative_utility = 0

    self.utility_his = [] # 保存自己的效用变化历史
    self.power_his = [] # 保存自己的能量变化历史
    #第0轮也就是一开始的数据
    self.utility_his.append(self.cumulative_utility)
    self.power_his.append(self.power)
    self.actionset = []

  #加入集合，重置效用
  def resetU(self):
    self.round = 0
    self.total = 0
    self.utility = 0
    self.expect = 0

  #清空动作集合
  def clearA(self):
    self.actionset = []

  def search_alternative(self,coas):
    self.clearA()
    for i in coas:
      if self.power >= ((i.ru.N * LossRate_BS(i.bs, i.ru) * i.ru.L) / (self.rate)) * self.pow:
        self.actionset.append(Action(i.ru, 0, -1))
      else:
        self.actionset.append(Action(i.ru, 1, -1))


