#coding=utf-8

from BaseStation import BS
from RegisterUser import RU
from FogDevice import FD
from Coalition import Coalition
import matplotlib.pyplot as plt
import datetime
import os

class NetworkController:
    def __init__(self, positions):
        self.bs, self.coalitions, self.fds = self.create_net(positions)
        self.path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today())
        # os.mkdir(self.path)  # 只mk 一次在net中mk

    def create_net(self, positions):
        bs = BS(positions["BS"])
        coalitions = self.set_coalitions(positions["RUs"], bs)
        fds = self.set_fds(positions["FDs"])

        return bs, coalitions, fds

    def set_coalitions(self, positions, bs):
        coalitions = []
        for i in range(len(positions)):
            ru = RU('RU%d' % (i + 1), positions[i])
            c = Coalition(bs, ru, i)
            c.bs = bs
            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % (i + 1), positions[i])
            fds.append(fd)
        return fds

    def show_coalitions(self, round):
        # 输出打印coalition
        # for i in self.coalitions:
        #     print i.ru.ruId #,"need power:",(i.ru.N * LossRate_BS(i.bs, i.ru) * i.ru.L / 100) * 0.004
        #     print "   RelaySet:",
        #     for j in i.RelaySet:
        #         print j.fdId,
        #     print
        #     print "   EHSet:",
        #     for j in i.EHSet:
        #         print j.fdId,
        #     print
        #     for j in i.fds:
        #         print "  ",j.fdId,"expect:",j.expect,"round:",j.round,"total:",j.total,"power:",j.power
        #    #print ""

        # 绘制图像保存
        #path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录

        plt.figure()
        colors = [ 'g', 'r', 'orange', 'blue', 'brown', 'teal'] #这里最多四种颜色
        cindex = 0
        # 按照联盟来打点的颜色
        for i in self.coalitions:
            plt.scatter(i.bs.position[0], i.bs.position[1], c='b')
            plt.annotate("BS", (i.bs.position[0], i.bs.position[1]))
            plt.scatter(i.ru.position[0], i.ru.position[1], c=colors[cindex])
            plt.annotate(i.ru.ruId, (i.ru.position[0], i.ru.position[1]))

            for j in i.RelaySet:
                plt.scatter(j.position[0], j.position[1], c=colors[cindex], marker='*')
                plt.annotate(j.fdId, (j.position[0], j.position[1]))

            for j in i.EHSet:
                plt.scatter(j.position[0], j.position[1], c=colors[cindex], marker='x')
                plt.annotate(j.fdId, (j.position[0], j.position[1]))

            cindex += 1
        plt.savefig("%s/round%s.png" % (self.path, round))  # 保存图片
        plt.close()

    def save_result(self,round):
        # path = 'Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录

        for i in self.fds:
            fig = plt.figure()

            plt.subplot(211)
            plt.xlabel('round')
            plt.ylabel('Power(J) of %s' % i.fdId)
            data_x = [j for j in range(0, round+1)]
            data_pow = i.power_his
            labelx = range(1, round+2)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_pow, marker='*', label='%s pow' % i.fdId)
            plt.legend()  # 给图像加上图例

            plt.subplot(212)
            plt.xlabel('round')
            plt.ylabel('Utility of %s' % i.fdId)
            data_x = [j for j in range(0, round+1)]
            data_utility = i.utility_his
            labelx = range(1, round+2)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_utility, marker='^', label='%s utility' % i.fdId)

            plt.legend()  # 给图像加上图例
            plt.tight_layout()  # 解决重叠问题
            fig.savefig("%s/%s.png" % (self.path, i.fdId))  # 保存图片
            plt.close()

    # def show_powerhis(self, round):
    #     #path = 'Pics/DynamicMultiRelay' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录
    #     for i in self.fds:
    #
    #
    # def show_utilityhis(self, round):

