#coding=utf-8
import random
class RU:
  def __init__(self, ruId, position):
    self.ruId = ruId
    self.position = position
    self.L = 1.0

    self.N = random.randint(20,40)
    #self.N = 30
    self.bandWidth = 0
    #初始每个Ru的cell都为空
    self.cell = []
    #Cell划分成两个集合交替进行信息和能量中继
    self.RelaySet = []
    self.EHSet = []
    #还需要记录基站到自己的丢包率，来计算自己最多丢失的数据包
    self.BS_RU_lossrate = 0.0
  def getset(self, n):
    if n == 0:
      return self.RelaySet
    else:
      return self.EHSet