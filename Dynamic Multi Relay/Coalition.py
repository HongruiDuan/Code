#coding=utf-8

from Utility import *
from Energy import energy

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
        #加入时考虑的应该是期望效用
        fd.expect = self.join_utility(fd, setnum) / 2
        # print fd.fdId, "join", self.ru.ruId, "set:", setnum, "join utility:", self.join_utility(fd,setnum)


    #在联盟中的效用
    #TODO:得出的计算结果不对，每一个RU那里算出来的数据包数目都是一样的
    def utility(self, fd, setnum):
        #计算通过当前集合能够得到的有效信息量
        solidInfo = 1
        e1 = LossRate_FDS_RU(self.bs, self.ru)
        l = 1
        for i in self.getset(setnum):
            l *= LossRate_BS(self.bs, i)

        if l == 1:
            solidInfo = self.ru.N * e1
        else:
            solidInfo = self.ru.N * e1 * (1 - l)
        # 计算该FD的效用
        w_fd = float(1 - LossRate_FDS_RU(self.bs, fd))
        w_total = 0.0
        for i in self.getset(setnum):
            # TODO:这里到底要不要乘后面从FD到RU的链路丢包率
            # w1 = (1 - LossRate_FDS_RU(i, self.bs))
            w_total += (1 - LossRate_FDS_RU(i, self.bs))

        #TODO:这里上面是已经算了在其中的效用的
        # w_total += w_fd

        n = int(float((w_fd / w_total)) * solidInfo)
        #print fd.fdId,"in ",self.ru.ruId,"Set:",setnum,"solidinfo:",solidInfo,"percentage",w_fd/w_total
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
        if l == 1:
            solidInfo = self.ru.N * e1
        else:
            solidInfo = self.ru.N * e1 * (1 - l)
        w_fd = (1 - LossRate_FDS_RU(self.bs, fd))
        w_total = 0.0
        for i in self.getset(setnum):
            # TODO:这里到底要不要乘后面从FD到RU的链路丢包率
            w_total += (1 - LossRate_FDS_RU(i, self.bs))

        #算上新加入的
        w_total += w_fd

        n = int((w_fd / w_total) * solidInfo)
        #print fd.fdId,"join",self.ru.ruId,"set:",setnum,"utility:",n
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
        #TODO:这里不用Id就会出现那种多次选择的问题
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
        fd.power += time * energy(fd,self.bs,1)
        fd.round += 1

    def relayMsg(self,fd):
        print fd.fdId,"in",fd.coalition.ru.ruId,"set:",fd.setchoice,"relayMsg"
        fd.power -= (fd.expect * self.ru.L / fd.rate) * 0.004
        fd.total += self.utility(fd, fd.setchoice)
        fd.round += 1

# 单元测试各个函数是否能够满足
if __name__ == 'main':
    pass