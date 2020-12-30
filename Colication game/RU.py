# coding=utf-8

import math
import random


from StackelbergGame import fds_game as fg


class RU:
    # todo: is value right
    def __init__(self, ruId,position):
        # 中继设备 host
        self.ruId, self.position = ruId, position