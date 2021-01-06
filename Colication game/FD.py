# coding=utf-8

import math
import random


import NetworkEnvironment as ne
from StackelbergGame import fds_game as fg


class FD:
    # todo: is value right
    def __init__(self, fdId, position,num, loss_rate=0.0, connect_range=80.0,
                 gains=0.0, f_bs=0.0, f_fd=0.0, N1=0.0, b=0.0, is_using=False,
                 W=2500000000.0, N=1.0, P_T=6.0206, G_T=0.0, G_R=0.0):
        # 中继设备 host
        self.fdId = fdId

        # 设备编号
        self.num = num

        #设备位置
        self.position = position
        # self.name = 'FD%2d' % num

        # 当前连接处于的联盟
        self.coalition = None

        # 连接范围
        self.connect_range = connect_range

        # 连接范围内的 RU
        self.nearby_rus = []

        # 丢包率
        self.loss_rate = loss_rate


        # 获取的收益
        self.gains = gains
        self.power = random.uniform(0.0005, 0.0010)
        self.cumulative_utility = 0
        # self.gains_his = []
        self.power_his = []
        self.utility_his = []  # 保存自己的效用变化历史
        # self.gains_his.append(self.gains)
        self.power_his.append(self.power)
        self.utility_his.append(self.cumulative_utility)
        self.f_bs = f_bs
        self.f_fd = f_fd
        self.N1 = N1
        self.b = b

        self.is_using = is_using
        self.gains = gains
        self.P_T = P_T
        self.G_R = G_R
        self.G_T = G_T
        self.W = W
        self.N = N

        # 累积效用



        # 在联盟内部被选择的优先度
        self.rank = 0

        # 能量历史记录
        self.history_power = [self.power]

    def swap(self, fd_b):
        c_a = self.coalition
        c_b = fd_b.coalition

        c_a.disconnect(self)
        c_b.disconnect(fd_b)

        self.join_coalition(c_b)
        fd_b.join_coalition(c_a)
        
    def join_coalition(self, coalition):
        self.coalition = coalition
        coalition.paired_fds.append(self)

        self.loss_rate = ne.cal_loss_rate(self)
        # self.N1, self.b, self.f_bs, self.f_fd = fg(1.0-self.loss_rate)
        # print 'fd %d loss rate %f' % (self.num, self.loss_rate)

    def harvest_energy(self, bs, time):
        staPosition = self.position

        apPosition = bs.position

        d = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)
        
        # c = 300000000.0
        # lamda = c / bs.rf_W
        # L = 0.8
        # P_R = bs.rf_p_t * bs.rf_g_t * bs.rf_g_r * (lamda**2) / (L*(4*math.pi*d)**2)
        P_t = 8000
        G_T = 2
        G_R = 2
        c = 300000000.0
        lamda = c / 900000000.0
        L = 0.8
        P_R = P_t * G_T * G_R * (lamda ** 2) / (L * (4 * math.pi * d) ** 2)

        power = P_R * time
        # print('energy',power)
        self.power += power
#        self.gains_his.append(self.gains)

        # self.cumulative_utility += self.N1
        self.utility_his.append(self.cumulative_utility)

        self.power_his.append(self.power)
        return power
    
    def forward_data(self):
        self.power -= self.N1 * 0.00004
        self.gains += self.f_fd
        self.cumulative_utility += self.N1

        self.utility_his.append(self.cumulative_utility)

        self.power_his.append(self.power)
