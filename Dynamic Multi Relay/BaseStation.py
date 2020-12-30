# coding=utf-8


class BS:
  def __init__(self, position):
    self.position = position
    #基站的发射功率为
    self.power = 3000
    #基站的广播速度为3M/b每秒
    self.rate = 3072