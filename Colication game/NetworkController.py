# -*- coding:utf-8 -*-

from RU import RU
import math
import random

from Coalition import Coalition

from FD import FD
from BS import BS


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

    def create_net(self, positions):



        #TODO:初始化工作需要改成不需要mininet的

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
            ru = RU('RU %d' % i, positions[i])

            c = Coalition(ru, i)
            c.bs = bs
            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % i, positions[i], i)
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

    #TODO:采用拓扑图来显示
    def show_coalitions(self, round):
        for coalition in self.coalitions:
            print 'coalitoin %d: ' % coalition.num
            print '    paired fds: ', [fd.num for fd in coalition.paired_fds]
            print '    nearby fds: ', [fd.num for fd in coalition.nearby_fds]
