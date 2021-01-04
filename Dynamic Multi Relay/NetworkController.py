#coding=utf-8

from BaseStation import BS
from RegisterUser import RU
from FogDevice import FD
from Coalition import Coalition
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
class NetworkController:
    def __init__(self,positions):
        self.bs, self.coalitions, self.fds = self.create_net(positions)


    def create_net(self, positions):

        bs = BS(positions["BS"])
        coalitions = self.set_coalitions(positions["RUs"], bs)
        fds = self.set_fds(positions["FDs"])

        return bs, coalitions, fds

    def set_coalitions(self, positions, bs):
        coalitions = []
        for i in range(len(positions)):
            ru = RU('RU%d' % i, positions[i])
            c = Coalition(bs, ru, i)
            c.bs = bs
            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % i, positions[i])
            fds.append(fd)
        return fds

    def show_coalitions(self):
        for i in self.coalitions:
            print i.ru.ruId #,"need power:",(i.ru.N * LossRate_BS(i.bs, i.ru) * i.ru.L / 100) * 0.004
            print "   RelaySet:",
            for j in i.RelaySet:
                print j.fdId,
            print
            print "   EHSet:",
            for j in i.EHSet:
                print j.fdId,
            print
            for j in i.fds:
                print "  ",j.fdId,"expect:",j.expect,"round:",j.round,"total:",j.total,"power:",j.power
            #print ""

    def save_result(self,round):
        path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录
        #os.mkdir(path) # 只mk 一次在net中mk
        for i in self.fds:
            fig = plt.figure()

            plt.subplot(211)
            plt.xlabel('round')
            plt.ylabel('Power(J) of %s' % i.fdId)
            data_x = [j for j in range(0, round)]
            data_pow = i.power_his
            labelx = range(0, round + 1)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_pow, marker='*', label='%s pow' % i.fdId)
            plt.legend()  # 给图像加上图例

            plt.subplot(212)
            plt.xlabel('round')
            plt.ylabel('Utility of %s' % i.fdId)
            data_x = [j for j in range(0, round)]
            data_utility = i.utility_his
            labelx = range(0, round + 1)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_utility, marker='^', label='%s utility' % i.fdId)

            plt.legend()  # 给图像加上图例
            plt.tight_layout()  # 解决重叠问题
            fig.savefig("%s/%s.png" % (path, i.fdId))  # 保存图片
            plt.close()

    # def show_powerhis(self, round):
    #     #path = 'Pics/DynamicMultiRelay' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录
    #     for i in self.fds:
    #
    #
    # def show_utilityhis(self, round):

