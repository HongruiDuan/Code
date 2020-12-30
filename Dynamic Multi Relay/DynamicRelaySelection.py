#coding=utf-8


from LossRate import *
from BaseStation import *
from FogDevice import FD
from RegisterUser import RU
from random import randint
from Utility import *
from Energy import energy
from Action import Action
from SequentialCusSelect import sequentialchoose
from math import pi,sqrt
import math
# ---------------------------------------------------------------------------------------#
#定义初始的联盟迭代变量
round = 10

#数据包大小
L = 1

def solidInfo(fd, ru, set):
    e1 = LossRate_FDS_RU(BS0, ru)
    l = 1

    for i in ru.getset(set):
        l *= LossRate_BS(BS0, i)

    l *= LossRate_BS(BS0, fd)
    if l == 1:
        return ru.N * e1
    else:
        return ru.N * e1 * (1 - l)

def utility(bs, fd, ru, set):
    #这里是没有BS实例的
    w_fd = (1 - LossRate_FDS_RU(bs, fd)) * (1 - LossRate_FDS_RU(fd, ru))
    w_total = 0.0
    for i in ru.getset(set):
        #TODO:这里到底要不要乘后面从FD到RU的链路丢包率
        w_total += (1 - LossRate_FDS_RU(i, bs)) * (1 - LossRate_FDS_RU(i, ru))
    if fd.choice != ru.ruId:
        w_total += w_fd
    #这里的有效信息计算有问题，应该是算加入之后的
    n = int(w_fd / w_total * solidInfo(fd, ru, 0))
    return n




if __name__ == '__main__':

    #---------------------------------------------------------------------------------------#
    # 初始化设备的地理位置和请求的数据量
    BS0 = BS(5, 45, 10)

    FD1 = FD("FD1", 25, 53)
    FD2 = FD("FD2", 30, 42)
    FD3 = FD("FD3", 35, 35)
    FD4 = FD("FD4", 20, 25)
    FD5 = FD("FD5", 15, 10)
    FDs = [FD1, FD2, FD3, FD4, FD5]

    RU1 = RU("RU1", 50, 50)
    RU2 = RU("RU2", 50, 10)
    RUs = [RU1, RU2]

    #FD向基站进行注册
    for i in FDs:
        #FD需要做什么呢
        print i.x,i.y
        i.BS_FD_lossrate = LossRate_BS(BS0, i)
    #RU向基站发送请求消息，
    for i in RUs:
        print i.x, i.y
        i.BS_RU_lossrate = LossRate_FDS_RU(BS0, i)



    #初始划分之后进行100轮传输，每10轮传输进行一次联盟调整
    cur_round = 0
    while cur_round < 100:

        #流程
        #1.基站广播每轮中给每个RU传输的数据包数目
        for i in RUs:
            i.N = randint(20, 30)

        #2.RU与联盟中的FD进行交互,判断哪些设备可以进行中继
        for i in RUs:
            #在知道了每轮传输的数据包数量之后就可以进行RelaySet和EHSet的更新了
            for j in i.RelaySet:
                if j.power < ((i.N * LossRate_BS(BS0,i) * L) / (j.rate)) * j.pow:
                    i.EHSet.append(j)
                i.RelaySet = [i.RelaySet[k] for k in range(0,len(i.RelaySet)) if i.RelaySet[k].power >= ((i.N * LossRate_BS(BS0,i) * L) / (i.RelaySet[k].rate)) * i.RelaySet[k].pow]
            for j in i.EHSet:
                if j.power >= ((i.N * LossRate_BS(BS0, i) * L) / (j.rate)) * j.pow:
                    i.RelaySet.append(j)
                i.EHSet = [i.EHSet[k] for k in range(0, len(i.EHSet)) if i.EHSet[k].power < ((i.N * LossRate_BS(BS0, i) * L) / (i.EHSet[k].rate))*i.EHSet[k].pow]

        #3.基站广播数据，FD进行能量收集，RU收集信息

        for i in RUs:
            for j in i.EHSet:
                #这里的根据每个RU请求的数据量来
                j.power += (i.N / BS0.rate) * energy(BS0, j ,1)
        #4.FD将自己接收到的信息传输给联盟中的RU,TODO:这里感觉需要实际模拟一下网络编码传输
        for i in RUs:
            for j in i.RelaySet:
                # 这里的根据每个RU请求的数据量来
                j.power -= (j.utility * L / j.rate) * 0.004
        #5.RU统计自身还缺失的数据包，向基站发送数据传输请求

        #6.基站给各个RU广播剩余的数据包 （这个过程还是存在丢包）TODO:这个过程的丢包率过大的话，将需要重复多次才能够结束这个流程
        #或者直接在下一轮中加入这个需要重传的数据包，还是让中继来一起接受


        #FD更新自己的期望效用
        for i in FDs:
            i.total += i.utility
            i.utility = 0


        #
        for i in FDs:
            i.round += 1


        #7.RU统计自己的效用之后调整自己的选择,每10轮进行一次
        if cur_round > 0 and cur_round % 10 == 0:
            cus = []
            for i in FDs:

                if i.total / i.round < i.expect:
                    cus.append(i)
                    if i.setchoice == 0:
                        i.choice.RelaySet = [i.choice.RelaySet[k] for k in range(0, len(i.choice.RelaySet)) if i.choice.RelaySet[k].fdId != i.fdId]
                    else:
                        i.choice.EHSet = [i.choice.EHSet[k] for k in range(0, len(i.choice.EHSet)) if i.choice.EHSet[k].fdId != i.fdId]
            #更新cus的action set
            for i in cus:
                #清空动作集合
                i.clearA()
                for j in RUs:
                    if i.power > ((j.N * LossRate_BS(BS0,j) * L) / (i.rate)) * i.pow:
                        #加入RelaySet
                        i.actionset.append(Action(j, 0, 0))
                    else:
                        i.actionset.append(Action(j, 1, 0))
            print "in round",cur_round,"cus:"
            for i in cus:
                print i.fdId
                for k in i.actionset:
                    print i.fdId,"alternative:",k.ru.ruId,"set:",k.set
            print "cus end"
            #新加入的顾客优先级最低,将顾客按照优先级排序

            #cus = sorted(cus, key = lambda x:x['F_BS'], reverse = True)

            #按照顺序就餐的中餐厅模型进行FD顺序选择,暴力递归的方法求解
            equrium_state = sequentialchoose(BS0, RUs, cus)#TODO:这里传入的是RUs,在选择的时候就已经会更新联盟

            print "cus change action"
            for m in cus:
                print m.fdId
                m.resetU()
                #重置顾客的期望效用
                m.expect = utility(BS0, m, m.choice, m.setchoice) / 2
            # for n in equrium_state:
            #     print [n.fdId for n in m.RelaySet], " ", [n.fdId for n in m.EHSet]

            #调整联盟
            # for (m,n) in cus,best_action:
            #     for k in RUs:
            #         if k.ruId == n.ru.ruId:
            #             k.getset(n.set).append(m)
            #调整完之后看看新的联盟划分
            print "in round", cur_round, "change devide:"
            for m in RUs:
                print [n.fdId for n in m.RelaySet], " ", [n.fdId for n in m.EHSet]

        cur_round += 1


    print "100 round end"