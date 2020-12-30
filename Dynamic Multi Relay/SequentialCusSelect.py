#coding=utf-8

from RegisterUser import RU
from FogDevice import FD
from BaseStation import BS
from LossRate import *
from Utility import *
from Action import Action
import copy

#顺序就餐的中餐厅算法模型求解
# @param: S,当前系统的状态 S = copy of [RU1, RU2]这样的一个集合，其中每个元素都应该是原本元素的备份
# @param: A,每个顾客的动作集合    这个可以放在每个顾客的类中保存起来，这样就不用作为一个单独的输入元素了
# @param: C,需要就餐的顾客序列

# @return: 返回一个RU的副本 or ruId，用于更新自己的选择

def sequentialchoose(bs,S,C):
    #记录自己每个动作的效用
    #TODO:deepcopy的问题到时候得提前注意一下,现在这里的C队列一直没有更新过

    for i in C:
        #print "cus",i.fdId ,"start sequential choose"
        for j in i.actionset:
            #i执行完动作之后判断待选择顾客是否为空
            # 得到新的顾客序列
            C_up = copy.deepcopy(C)
            S_up = copy.deepcopy(S)
            #从原始顾客序列中去除自己
            for k in S_up:
                if k.ruId == i.choice.ruId:
                    if i.setchoice == 0:
                        k.RelaySet = [k.RelaySet[m] for m in range(0, len(k.RelaySet)) if k.RelaySet[m].fdId != i.fdId]
                    else:
                        k.EHSet = [k.EHSet[m] for m in range(0, len(k.EHSet)) if k.EHSet[m].fdId != i.fdId]
            #
            for k in S_up:
                if k.ruId == j.ru.ruId:
                    k.getset(j.set).append(i)

            for k in C_up:
                if k.fdId == i.fdId:
                    for m in range(0, len(S_up)):
                        if S_up[m].ruId == j.ru.ruId:
                            k.choice = S_up[m]
                            k.setchoice = j.set

            #更新完状态之后，调整顾客序列
            C_up = [C_up[k] for k in range(0, len(C_up)) if C_up[k].fdId != i.fdId]

            if len(C_up) == 0:
                #已经达到了nash均衡状态
                #更新当前的状态
                S_star = S_up
                ru_star  = 0
                for k in S_star:
                    if k.ruId == j.ru.ruId:
                        ru_star = k
                #采用该动作达到的最终效用

                U_x = utility(bs, i, ru_star,j.set)
                j.utility = U_x
            else:
                #不为空的时候需要迭代计算到最终的效用方程中
                # S_up = copy.deepcopy(S)
                # for k in S_up:
                #     if k.ruId == i.choice.ruId:
                #         if i.setchoice == 0:
                #             k.RelaySet = [k.RelaySet[m] for m in range(0,len(k.RelaySet)) if k.RelaySet[m].fdId!= i.fdId]
                #         else:
                #             k.EHSet = [k.EHSet[m] for m in range(0, len(k.EHSet)) if k.EHSet[m].fdId != i.fdId]
                #     if k.ruId == j.ru.ruId:
                #         k.getset(j.set).append(i)

                #得到新的顾客序列
                # C_up = copy.deepcopy(C)
                # C_up = [C_up[k] for k in range(0,len(C_up)) if C_up[k].fdId != i.fdId ]
                # for k in C_up:
                #     if k.fdId == i.fdId:
                #         for m in range(0,len(S_up)):
                #             if S_up[m].ruId == j.ru.ruId:
                #                 k.choice = S_up[m]
                #                 k.setchoice = j.set


                #这里还是返回自己的最终状态比较合适，那如果是返回的最终状态，返回了之后还需要将那些加入到ru的Id中，，可以直接计算最终效用，如果是返回动作的话
                S_star = sequentialchoose(bs, S_up, C_up)
                #TODO:这里递归调用的话是会让递归函数选择的，但是更新的是副本啊

                ru_star = 0
                for k in S_star:
                    if k.ruId == j.ru.ruId:
                        ru_star = k
                #这里要计算效用,需要知道最终自己选择的那个RU的集合中有多少个设备在做中继,有多少个设备在收集能量，需要每个RU的中继集合和能量收集集合
                #这里只需要计算最终的效用
                U_x = utility(bs, i, ru_star, j.set)
                j.utility = U_x
        #每个顾客从当前的最终动作中选出自己的最终动作
        a_star = Action(0,0,0)
        for k in i.actionset:
            if(k.utility > a_star.utility):
                a_star = k
        #print "a_star",a_star
        #TODO:这里如果传过来的是RUs而不是备份的话，在那边应该是已经添加进去了
        #先把待选择顾客从原始集合中剔除
        for k in S:
            if k.ruId == i.choice.ruId:
                if i.setchoice == 0:
                    k.RelaySet = [k.RelaySet[m] for m in range(0, len(k.RelaySet)) if k.RelaySet[m].fdId != i.fdId]
                else:
                    k.EHSet = [k.EHSet[m] for m in range(0, len(k.EHSet)) if k.EHSet[m].fdId != i.fdId]
        for k in S:
            if k.ruId == a_star.ru.ruId:
                k.getset(a_star.set).append(i)
                i.choice = k
                i.setchoice = a_star.set
        #直接遍历到下一个
        C = [C[k] for k in range(0,len(C)) if C[k].fdId != i.fdId]
        #print "cus",i.fdId ,"choose",a_star.ru.ruId," set:",a_star.set
        #A.append(a_star)

    #但是上面递归返回的最终的状态S
    return  S