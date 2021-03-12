# -*- coding:utf-8 -*-

from RU import RU
import math
import random

from Coalition import Coalition

from FD import FD
from BS import BS

import matplotlib.pyplot as plt
import datetime
import os

# 线程函数
def command(host, arg):
    result = host.cmd(arg)
    return result


#TODO:修改mininet中的相关api
class NetworkController:
    #这里是根据传入的位置来生成
    def __init__(self, positions):
        self.bs, self.coalitions, self.fds = self.create_net(positions)
        self.set_nearby_device()
        self.path = '../Pics/CoalicationGame/' + str(datetime.date.today())
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)  # 只mk 一次在net中mk

        self.utility_his = [0]
        self.fairness_his = [0]

    def create_net(self, positions):
        bs = BS(positions['BS'])

        coalitions = self.set_coalitions(positions['rus'], bs)
        fds = self.set_fds(positions['fds'])

        return bs, coalitions, fds

    def start_net(self):
       pass

    def start_game(self, game, round, max_round):
        game.start(round, max_round)

    def set_coalitions(self, positions, bs):
        coalitions = []
        for i in range(len(positions)):
            ru = RU('RU %d' % (i+1), positions[i])
            c = Coalition(ru, (i+1))
            c.bs = bs
            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % (i+1), positions[i], (i+1))
            fds.append(fd)
        return fds

    '''
    搜寻附近可连接的设备
    '''

    def set_nearby_device(self):
        for coalition in self.coalitions:
            coalition.bs = self.bs
            for fd in self.fds:
                p_ru = coalition.ru.position
                p_fd = fd.position
                if fd.connect_range >= math.sqrt((p_ru[0] - p_fd[0]) ** 2 + (p_ru[1] - p_fd[1]) ** 2): 
                    coalition.nearby_fds.append(fd)
                    fd.nearby_rus.append(coalition)

    def show_fds(self):
        # 打印中继设备的信息
        for fd in self.fds:
            if fd.coalition is not None:
                print 'fd %d: ' % fd.num
                print '    gains, power: %f, %f' % (fd.gains, fd.power)
                print '    f_bs, f_fd: %f, %f' % (fd.f_bs, fd.f_fd)

    def gains_per_round(self, round):
        total = 0.0
        for i in self.fds:
            total += i.cumulative_utility
        self.utility_his.append(total)

    # 先算每个联盟的fairness,然后再算整个系统的fairness

    def cal_fairness(fds):
        U_total = 0
        U_link_s = 0
        for i in range(0, len(fds)):
            U_total += fds[i].gains
            U_link_s += (1 - fds[i].loss_rate)
        X = []
        for i in range(0, len(fds)):
            Ui_overline = ((1 - fds[i].loss_rate) / U_link_s) * U_total
            if fds[i].gains <= Ui_overline:
                X.append(fds[i].gains / Ui_overline)
            else:
                X.append(1.0)
        sum_of_xi = 0
        for i in range(0, len(X)):
            sum_of_xi += X[i]

        sum_of_xi2 = 0
        for i in range(0, len(X)):
            sum_of_xi2 += X[i] ** 2

        fairness = (sum_of_xi) ** 2 / (len(X) * sum_of_xi2)
        return fairness

    def save_result(self,maxround):
        # path = 'Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录

        for i in self.fds:
            fig = plt.figure()

            plt.subplot(211)
            plt.xlabel('slot')
            plt.ylabel('Power(J) of %s' % i.fdId)
            data_x = [j for j in range(0, maxround+1)]
            data_pow = i.power_his
            labelx = range(0, maxround+1)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_pow, marker='*', label='%s pow' % i.fdId)
            plt.legend()  # 给图像加上图例

            plt.subplot(212)
            plt.xlabel('slot')
            plt.ylabel('Utility of %s' % i.fdId)
            data_x = [j for j in range(0, maxround+1)]
            data_utility = i.utility_his
            labelx = range(0, maxround+1)
            plt.xticks(data_x, labelx, fontsize=14)
            plt.plot(data_x, data_utility, marker='^', label='%s utility' % i.fdId)

            plt.legend()  # 给图像加上图例
            plt.tight_layout()  # 解决重叠问题
            fig.savefig("%s/%s.png" % (self.path, i.fdId))  # 保存图片
            plt.close()

        # 绘制总的效用变化 和 fairness变化曲线
        plt.figure()
        plt.xlabel('slot')
        plt.ylabel('Total Utility of all FDs')
        data_x = [j for j in range(0, maxround+1)]
        data_y1 = self.utility_his
        plt.xticks(data_x, labelx, fontsize=14)
        plt.plot(data_x, data_y1, marker='^', label='Throughput')
        plt.legend()  # 给图像加上图例
        plt.savefig("%s/Throughput per slot.png" % (self.path))  # 保存图片
        plt.close()

    def show_coalitions(self, round):
        for coalition in self.coalitions:
            print 'coalitoin %d: ' % coalition.num
            print '    paired fds: ', [fd.num for fd in coalition.paired_fds]
            print '    nearby fds: ', [fd.num for fd in coalition.nearby_fds]

        plt.figure()
        colors = ['g', 'r', 'orange', 'blue', 'brown', 'teal']  # 这里最多四种颜色
        cindex = 0
        # 按照联盟来打点的颜色
        plt.scatter(self.bs.position[0], self.bs.position[1], c='b', marker='o')
        plt.annotate("BS", (self.bs.position[0], self.bs.position[1]))

        for i in self.coalitions:
            plt.scatter(i.ru.position[0], i.ru.position[1], c=colors[cindex])
            plt.annotate(i.ru.ruId, (i.ru.position[0], i.ru.position[1]))
            for j in i.paired_fds:
                if j != i.selected_fd:
                    plt.scatter(j.position[0], j.position[1], c=colors[cindex], marker='+')
                    plt.annotate(j.fdId, (j.position[0], j.position[1]))
                else:
                    plt.scatter(j.position[0], j.position[1], c=colors[cindex], marker='*')
                    plt.annotate(j.fdId, (j.position[0], j.position[1]))

            cindex += 1
        plt.savefig("%s/round%s.png" % (self.path, round))  # 保存图片
        plt.close()
