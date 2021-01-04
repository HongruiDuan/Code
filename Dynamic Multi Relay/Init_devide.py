#coding=utf-8

#输入初始的ru和fd,输出最终的初始联盟划分
#
from random import randint
from LossRate import *
class Init_devide:
    def __init__(self, coalitions, fds):
        self.coalitions = coalitions
        self.fds = fds
        #print len(fds),len(self.coalitions)

    def random_devide(self):
        for i in self.fds:
            l = int(len(self.coalitions)) - 1
            i.coalition = self.coalitions[randint(0, l)]
            i.setchoice = randint(0, 1)
            i.coalition.join_coa(i,i.setchoice)

        #     l = int(len(self.coalitions)) - 1
        #     i.coalition = self.coalitions[randint(0, l) ]
        #     i.setchoice = randint(0, 1)
        # for i in self.fds:
        #     i.coalition.getset(i.setchoice).append(i)
        print "random initial divide:"
        for i in self.coalitions:
            print(i.ru.ruId)
            print "   RelaySet:"
            for j in i.getset(0):
                print "     ",j.fdId,
            print #换行
            print "    EHSet:"
            for j in i.getset(1):
                print "     ",j.fdId,
            print #换行
    def simultan_cus(self):
        bestResponse = True
        round = 0
        while (bestResponse and round < 10):
            #print round
            bestResponse = False
            for i in self.fds:
                for j in self.coalitions:
                    # FD的能量满足当前RU的需要
                    # print i.fdId,"have:",i.power," ",j.ruId,"need power:",((j.N * LossRate_BS(BS0,j) * L) / (i.rate))* i.pow
                    if i.coalition.ru.ruId != j.ru.ruId and i.power >= (
                            (j.ru.N * LossRate_BS(j.bs, j.ru) * j.ru.L) / (i.rate)) * i.pow and j.join_utility(i, 0) > i.coalition.utility(i):
                        #print i.fdId,"from",i.coalition.ru.ruId,"Set",i.setchoice ,"to",j.ru.ruId,"Set 0"
                        # 比较加入中继集合的效用
                        i.coalition.exit_coa(i)
                        i.coalition, i.setchoice = j, 0
                        # 加入联盟的时候确定期望效用
                        j.join_coa(i, 0)
                        bestResponse = True
                    # 当前FD的能量不满足RU的需求
                    elif i.coalition.ru.ruId != j.ru.ruId and i.power < (
                            (j.ru.N * LossRate_BS(j.bs, j.ru) * j.ru.L) / (i.rate)) * i.pow and j.join_utility(i, 1) > i.coalition.utility(i):
                        # 比较加入能量收集能量的集合的效用
                        #print i.fdId, "from",i.coalition.ru.ruId,"Set",i.setchoice ,"to", j.ru.ruId, "Set 1"
                        i.coalition.exit_coa(i)
                        i.coalition, i.setchoice = j, 1
                        j.join_coa(i, 1)
                        bestResponse = True
                    else:
                        pass
            round += 1
        print "simultan_cus end"


    def print_devide(self):
        print "init devide"
        for i in self.coalitions:
            print " ", i.ru.ruId, "packet num:", i.ru.N, "need power:",((i.ru.N * LossRate_BS(i.bs, i.ru) * i.ru.L) / (100)) * 0.004
            print "    RelaySet:"
            # print "     ",
            for j in i.getset(0):
                print "     ", j.fdId,"in",j.coalition.ru.ruId," ",j.setchoice,"power:",j.power,"utility:",i.utility(j)
            #print
            print "    EHSet:"
            # print "     ",
            for j in i.getset(1):
                print "     ", j.fdId,"in",j.coalition.ru.ruId," ",j.setchoice,"power:", j.power,"utility:",i.utility(j)
            #print
