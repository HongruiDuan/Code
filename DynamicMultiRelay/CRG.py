#coding=utf-8

from RegisterUser import RU
from FogDevice import FD
from LossRate import *
from copy import deepcopy
from Action import Action
from Params import *

class CRG:
    def __init__(self, cus, coas):
        self.customers = cus
        self.coalitions = coas

    def simultan_cus(self):
        bestResponse = True
        round = 0
        while (bestResponse and round < 50):
            bestResponse = False
            for i in self.fds:
                for j in self.coalitions:
                    # FD的能量满足当前RU的需要
                    distance = sqrt((i.position[0] - j.ru.position[0]) ** 2 + (i.position[1] - j.ru.position[1]) ** 2)
                    # print i.fdId,"have:",i.power," ",j.ruId,"need power:",((j.N * LossRate_BS(BS0,j) * L) / (i.rate))* i.pow
                    if i.coalition.ru.ruId != j.ru.ruId and distance < D2D_dis_limit and i.power >= (
                            (j.ru.N * LossRate_BS(j.bs, j.ru) * j.ru.L) / (i.rate)) * i.pow and j.join_utility(i,0) > i.coalition.utility(i):
                        # 比较加入中继集合的效用
                        i.coalition.exit_coa(i)
                        i.coalition, i.setchoice = j, 0
                        # 加入联盟的时候确定期望效用
                        j.join_coa(i, 0)
                        bestResponse = True
                    # 当前FD的能量不满足RU的需求
                    elif i.coalition.ru.ruId != j.ru.ruId and distance < D2D_dis_limit and i.power < (
                            (j.ru.N * LossRate_BS(j.bs, j.ru) * j.ru.L) / (i.rate)) * i.pow and j.join_utility(i,1) > i.coalition.utility(i):
                        # 比较加入能量收集能量的集合的效用
                        i.coalition.exit_coa(i)
                        i.coalition, i.setchoice = j, 1
                        j.join_coa(i, 1)
                        bestResponse = True
                    else:
                        pass
            round += 1
        return self.coalitions

    #用一个递归函数去达到最终的状态，但是原函数做的选择还是原来的，最终返回的也是原来的函数



    #不论是顺序选择还是同时就餐，都暂时还没有考虑到能量的限制
    # TODO:顺序就餐调整的时候，没有考虑到距离限制
    def sequentialChoose(self):
        t_cus = deepcopy(self.customers)
        t_coas = deepcopy(self.coalitions)

        final_coalications = self.greedy_predict(t_cus, t_coas)

        #想一想最终的算法流程再写吧，想清楚先

        for i in self.customers:
            flag = True
            for j in i.actionset:
                if flag == False:
                    break
                for k in final_coalications:
                    if k.ru.ruId == j.ru.ruId:
                        i.actionset = [i.actionset[m] for m in range(len(i.actionset)) if i.actionset[m].ru.ruId == k.ru.ruId]
                        print "after sequencial:", i.fdId,"size:", len(i.actionset), i.actionset[0].ru.ruId, i.actionset[0].set
                        flag = False
        #上面得到了每个人的最优动作，后面是依次选择得到最终的联盟分布

        for i in self.customers:
            print i.fdId, "exit", i.coalition.ru.ruId, "set:", i.setchoice,"action size",len(i.actionset)
            i.coalition.exit_coa(i)
            for j in self.coalitions:
                if j.ru.ruId == i.actionset[0].ru.ruId:
                    print i.fdId, "choose", j.ru.ruId, "set:", i.actionset[0].set
                    j.join_coa(i, i.actionset[0].set)

        return self.coalitions


    def predict(self, cus, coas, depth):
        for i in cus:
            for j in i.actionset:
                print "in", depth,"cus", i.fdId, "start sequential choose", j.ru.ruId, "set", j.set
                # i执行完动作之后判断待选择顾客是否为空
                # 得到新的顾客序列
                C_up = deepcopy(cus)
                S_up = deepcopy(coas)
                # 从原始顾客序列中去除自己，这里在前面加入到顾客序列的时候就已经退出了,不对.应该是在预测的时候退出
                for k in S_up:
                    if k.ru.ruId == i.coalition.ru.ruId:
                        k.exit_coa(i)
                for k in S_up:
                    if k.ru.ruId == j.ru.ruId:
                        k.join_coa(i, j.set)
                # 更新完状态之后，调整顾客序列
                C_up = [C_up[k] for k in range(0, len(C_up)) if C_up[k].fdId != i.fdId]
                if len(C_up) == 0:
                    S_star = S_up
                    coa_star = None
                    for k in S_star:
                        if k.ru.ruId == j.ru.ruId:
                            coa_star = k
                    U_x = coa_star.utility(i)
                    j.utility = U_x
                else:
                    S_star = self.predict(C_up, S_up, depth + 1)
                    coa_star = None
                    for k in S_star:
                        if k.ru.ruId == j.ru.ruId:
                            coa_star = k
                    U_x = coa_star.utility(i)
                    j.utility = U_x
            # 每个顾客从当前的最终动作中选出自己的最终动作
            a_star = Action(None,0,-1.0)
            for k in i.actionset:
                if (k.utility > a_star.utility):
                    a_star = k
            for k in coas:
                if k.ru.ruId == i.coalition.ru.ruId:
                    k.exit_coa(i)
            for k in coas:
                if a_star.ru is not None and k.ru.ruId == a_star.ru.ruId:
                    k.getset(a_star.set).append(i)
                    i.coalition = k
                    i.setchoice = a_star.set
            # 直接遍历到下一个
            #cus = [cus[k] for k in range(0, len(cus)) if cus[k].fdId != i.fdId]

        return coas


    def greedy_predict(self, cus, coas):
        for i in cus:
            for j in i.actionset:
                for k in coas:
                    if k.ru.ruId == j.ru.ruId:
                        j.utility = k.join_utility(i, j.set)
            # 从自己的动作集合之中选出
            a_star = Action(None, 0, -1.0)
            for j in i.actionset:
                distance = sqrt((i.position[0] - j.ru.position[0]) ** 2 + (i.position[0] - j.ru.position[0]) ** 2)
                if (j.utility > a_star.utility) and distance < D2D_dis_limit:
                    a_star = j
            for j in coas:
                if a_star.ru is not None and j.ru.ruId == a_star.ru.ruId:
                    j.join_coa(i, a_star.set)
        return coas