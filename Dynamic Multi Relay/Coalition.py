#coding=utf-8

from Utility import *
from Energy import energy
from copy import deepcopy




class Coalition:
    def __init__(self,bs,ru,coaId):
        self.bs, self.ru, self.coaId = bs, ru, coaId
        self.fds, self.RelaySet, self.EHSet = [], [], []


    def getset(self, num):
        if num == 0:
            return self.RelaySet
        else:
            return self.EHSet

    def join_coa(self, fd, setnum):
        self.fds.append(fd)
        self.getset(setnum).append(fd)
        fd.coalition = self
        fd.setchoice = setnum
        fd.resetU()
        #加入时考虑的应该是期望效用,乘以系数的话，系数该如何确定呢
        fd.expect = self.join_utility(fd, setnum) * 0.8
        # print fd.fdId, "join", self.ru.ruId, "set:", setnum, "join utility:", self.join_utility(fd,setnum)


    #在联盟中的效用

    def utility(self, fd):
        #计算通过当前集合能够得到的有效信息量
        solidInfo = 1
        e1 = LossRate_FDS_RU(self.bs, self.ru)
        l = 1
        for i in self.getset(fd.setchoice):
            l *= LossRate_BS(self.bs, i)

        if l == 1:
            solidInfo = self.ru.N * e1
        else:
            solidInfo = self.ru.N * e1 * (1 - l)
        # 计算该FD的效用
        w_fd = float(1 - LossRate_FDS_RU(self.bs, fd))
        w_total = 0.0
        for i in self.getset(fd.setchoice):

            # w1 = (1 - LossRate_FDS_RU(i, self.bs))
            w_total += (1 - LossRate_FDS_RU(i, self.bs))

        n = int(float((w_fd / w_total)) * solidInfo)
        # print fd.fdId,"in ",self.ru.ruId,"Set:",fd.setchoice,"solidinfo:",solidInfo,"percentage",w_fd/w_total,"utility",n
        return n

    #加入联盟的效用还是需要重新计算
    def join_utility(self, fd, setnum):
        # 计算通过当前集合能够得到的有效信息量
        solidInfo = 1
        e1 = LossRate_FDS_RU(self.bs, self.ru)
        l = 1
        for i in self.getset(setnum):
            l *= LossRate_BS(self.bs, i)

        #算上新加入的
        l *= LossRate_BS(self.bs, fd)
        # print "l:",l,"e1:",e1
        if l == 1:
            solidInfo = self.ru.N * e1
        else:
            solidInfo = self.ru.N * e1 * (1 - l)

        # 这里是距离基站太远的设备丢包率太大了
        w_fd = (1 - LossRate_BS(self.bs, fd))
        w_total = 0.0
        for i in self.getset(setnum):

            w_total += (1 - LossRate_FDS_RU(i, self.bs))

        #算上新加入的
        w_total += w_fd
        # print fd.fdId, "join", self.ru.ruId, "set:", setnum, w_fd, " ", w_total, " ", solidInfo
        n = int((w_fd / w_total) * solidInfo)
        # print fd.fdId,"join",self.ru.ruId,"set:",setnum,"utility:",n
        return n

    def exit_coa(self,fd):
        # print fd.fdId, "exit", self.ru.ruId, "set:", fd.setchoice
        # print "    before:",
        # for i in self.getset(fd.setchoice):
        #     print i.fdId,
        # print
        #保存一下
        t = fd.setchoice
        for i in range(len(self.fds)):
            if self.fds[i] == fd:
                fd.coalition = None
                fd.setnum = -1

        self.fds = [self.fds[j] for j in range(len(self.fds)) if self.fds[j].fdId != fd.fdId]
        self.RelaySet = [self.RelaySet[j] for j in range(len(self.RelaySet)) if self.RelaySet[j].fdId != fd.fdId]
        self.EHSet = [self.EHSet[j] for j in range(len(self.EHSet)) if self.EHSet[j].fdId != fd.fdId]
        # print "    after:",
        # for i in self.getset(t):
        #     print i.fdId,
        # print



    def get_enough_power_fds(self):
        self.EHSet = []
        self.RelaySet = []
        for fd in self.fds:
            if fd.power < ((self.ru.N * LossRate_BS(self.bs,fd) * self.ru.L) / (fd.rate)) * fd.pow:
                self.EHSet.append(fd)
            else:
                self.RelaySet.append(fd)

    def harvestEnergy(self, fd, time):
        power_harvest = time * energy(fd, self.bs, 1)
        fd.utility = 0

        fd.power += power_harvest
        fd.power_his.append(fd.power)
        fd.utility_his.append(fd.cumulative_utility)

        fd.round += 1
        print fd.fdId, "in time", time, "harvest energy:", power_harvest


    def relayMsg(self,fd):
        # print fd.fdId,"choose", fd.coalition.ru.ruId,"set:",fd.setchoice
        # for i in fd.coalition.getset(fd.setchoice):
        #     print i.fdId,
        # print
        # utility表示的是在当前这一轮中的收益
        fd.utility = self.utility(fd)
        fd.total += fd.utility

        fd.cumulative_utility += fd.utility
        fd.utility_his.append(fd.cumulative_utility)



        power_cost = (fd.utility * self.ru.L / fd.rate) * 0.004
        fd.power -= power_cost
        fd.power_his.append(fd.power)
        #这里计算实际效用的时候
        fd.round += 1

        print fd.fdId, "in", fd.coalition.ru.ruId, "set:", fd.setchoice, "relayMsg num", fd.utility, "cost power:", power_cost



    def alter_coalition(self):
        t_RelaySet = deepcopy(self.RelaySet)
        t_EHSet = deepcopy(self.EHSet)
        self.RelaySet = []
        self.EHSet = []
        for i in t_RelaySet:
            if i.power < (self.ru.N * LossRate_BS(self.bs, self.ru) * self.ru.L / i.rate) * i.pow:
                for j in self.fds:
                    if j.fdId == i.fdId:
                        self.EHSet.append(j)
                        j.setchoice = 1
                        break
            elif i.power >= (self.ru.N * LossRate_BS(self.bs, self.ru) * self.ru.L / i.rate) * i.pow:
                for j in self.fds:
                    if j.fdId == i.fdId:
                        self.RelaySet.append(j)
                        j.setchoice = 0
                        break
        for i in t_EHSet:
            if i.power >= (self.ru.N * LossRate_BS(self.bs, self.ru) * self.ru.L / i.rate) * i.pow:
                for j in self.fds:
                    if j.fdId == i.fdId:
                        self.RelaySet.append(j)
                        j.setchoice = 0
                        break
            elif i.power < (self.ru.N * LossRate_BS(self.bs, self.ru) * self.ru.L / i.rate) * i.pow:
                for j in self.fds:
                    if j.fdId == i.fdId:
                        self.EHSet.append(j)
                        j.setchoice = 1
                        break

# 单元测试各个函数是否能够满足
if __name__ == 'main':

    pass