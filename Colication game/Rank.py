# -*- coding:utf-8 -*-
import math
import random
import matplotlib.pyplot as plt
import json
import os


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
import numpy as np
np.set_printoptions(suppress=True)
import thread
import threading
import time

global min_x
global max_x

'''
paired_fds:是所有设备池
valid_fds:候选满足传输能量的设备池
'''
def Fairness(paired_fds,valid_fds,x): #x表示的是传入设备的编号，也即染色体
    #传入的x是浮点数，要转化成整数
    x = int(round(x))
    if x >= len(valid_fds):
        x = len(valid_fds) - 1
    U_total = 0
    U_link_s = 0     
    for i in range(0,len(paired_fds)):
        U_total += paired_fds[i].gains
        U_link_s += (1-paired_fds[i].loss_rate)
    #加上采用第i个中继设备时的收益来计算fairness
    U_total += valid_fds[x].f_fd
    X=[]
    for i in range(0,len(paired_fds)):
        Ui_overline = ((1-paired_fds[i].loss_rate)/U_link_s)*U_total
        if paired_fds[i].num == valid_fds[x].num:
            if (paired_fds[i].gains+valid_fds[x].f_fd)<=Ui_overline:
                X.append(paired_fds[i].gains/Ui_overline)
            else:
                X.append(1.0)
        elif paired_fds[i].gains<=Ui_overline:
            X.append(paired_fds[i].gains/Ui_overline)
        else:
            X.append(1.0)
    sum_of_xi = 0
    for i in range(0,len(X)):
        sum_of_xi += X[i]

    sum_of_xi2 = 0
    for i in range(0,len(X)):
        sum_of_xi2 += X[i]**2

    fairness = (sum_of_xi)**2/(len(X)*sum_of_xi2)
    # paired_fds[x].fairness = fairness
    return fairness
#第二个目标函数，传输参数为序号
def Utility(valid_fds,x):
    x= int(round(x))
    if x>= len(valid_fds):
        x = len(valid_fds)-1
    value = valid_fds[x].f_bs
    return value

def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1
#按照function的值来排序
#list1的含义
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1: #values中最小值的下标
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = float('inf')
    return sorted_list
#NSGA-II's fast non dominated sort,基于帕雷托最优解来计算支配解集
'''
输入：目标1数组，目标2数组

输出：前沿面数组，每一个前沿面中包含的是设备序号

'''
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]
    #对于目标1中的每一个解，计算其支配解集和支配解的个数
    for p in range(0,len(values1)):
        S[p]=[] #p的支配集合
        n[p]=0  #p的支配个数
        for q in range(0, len(values1)):
            #第p个设备的第一个目标大于q
            if  (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            #如果一个解被其他解所支配，那么其被支配数+1
            elif (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        #如果一个解的被支配数为0
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if( n[q]==0 ):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front)-1]
    return front
#采用解的距离有问题，不采用归一化两个目标之间距离差值太大，采用标准化，不能从初始值0开始
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    #距离计算公式，换种定义
    for k in range(1,len(front)-1):
        if max(values1) == min(values1):
            maxdis = 1
        else:
            maxdis = max(values1)-min(values1)
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values1[sorted1[k-1]])/maxdis #统一标准化
    for k in range(1,len(front)-1):
        if max(values2) == min(values2):
            maxdis = 1
        else:
            maxdis = max(values2)-min(values2)
        distance[k] = distance[k]+ (values2[sorted2[k+1]] - values2[sorted2[k-1]])/maxdis
    return distance

#交叉
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#突变
def mutation(solution):
    global max_x
    mutation_prob = random.random()
    if max_x == min_x:
        maxdis = 1
    else:
        maxdis = max_x-min_x
    if mutation_prob <1:
        solution = min_x+maxdis*random.random()
    return solution

'''
排序函数,供考虑fairness时调用
输入：已知博弈信息后的设备池paired_fds(已经按照基站的收益进行了排序)
计算：采用各个解能够达到的两个目标的大小来对各个中继设备来进行排序
输出:已经更新了Rank值的设备池paired_fds

'''
def Rank(paired_fds,valid_fds):

    #只用求出所有中继设备的rank值不需要进行遗传求出最优解
    # obj1 = [Utility(i) for i in range(0,len(paired_fds))]
    # obj2 = [Fairness(i) for i in range(0,len(paired_fds))]
    # front = fast_non_dominated_sort(obj1[:],obj2[:])
    # print(front)
    # for i in range(0,len(front)):
    #     for j in range(0,len(front[i])):
    #         paired_fds[front[i][j]].rank = i
    # # for i in range(0,len(paired_fds)):
    # #     print(paired_fds[i].rank)        
    # return paired_fds
    '''
    在求解帕累托前沿面之前,将能量不充足的设备从解集中删除掉
    计算fairness的时候需要考虑的是所有设备的效益
    但是求解时不考虑
    '''
    pop_size = len(paired_fds)
    max_gen = 20
    #初始化
    global min_x
    global max_x
    min_x = 0
    max_x = len(valid_fds)-1
    #random.random()产生一个(0,1)的随机数,此处在X范围内随机产生一个数
    solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)] #产生从0到20设备编号解
    gen_no=0
    result=[]
    while(gen_no<max_gen):
        fairness_values = [Fairness(paired_fds,valid_fds,solution[i])for i in range(0,pop_size)]
        utility_values = [Utility(valid_fds,solution[i])for i in range(0,pop_size)]
        
        # print(fairness_values)
    
        # print(utility_values)
        non_dominated_sorted_solution = fast_non_dominated_sort(utility_values[:],fairness_values[:])#快速非支配排序返回的front的集合
        # print("第",gen_no, "次繁衍的帕累托最优的设备编号为")
            
        # for valuez in non_dominated_sorted_solution[0]:
            # print(round(solution[valuez],3),end=" ")
        # print("\n")
        crowding_distance_values=[]
        for i in range(0,len(non_dominated_sorted_solution)):
            crowding_distance_values.append(crowding_distance(utility_values[:],fairness_values[:],non_dominated_sorted_solution[i][:]))
        solution2 = solution[:]
        #产生子代
        while(len(solution2)!=2*pop_size): #新一代种群数量是原种群数量的两倍
            a1 = random.randint(0,pop_size-1) #从种群中随机选择两个个体
            b1 = random.randint(0,pop_size-1)
            solution2.append(crossover(solution[a1],solution[b1]))#从原始的两个个体中交叉产生新的个体
        fairness_values2 = [Fairness(paired_fds,valid_fds,solution2[i])for i in range(0,2*pop_size)]
        utility_values2 = [Utility(valid_fds,solution2[i])for i in range(0,2*pop_size)]
        non_dominated_sorted_solution2 = fast_non_dominated_sort(utility_values2[:],fairness_values2[:])
        crowding_distance_values2=[]
        for i in range(0,len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(crowding_distance(utility_values2[:],fairness_values2[:],non_dominated_sorted_solution2[i][:]))
        new_solution= []
        for i in range(0,len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i]) for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
            front.reverse()
            for value in front:
                new_solution.append(value)
                if(len(new_solution) == pop_size):
                    break
            if (len(new_solution) == pop_size):
                break
        solution = [solution2[i] for i in new_solution] # 最中求解出来的solution           
        result = solution 
        gen_no = gen_no + 1   
    IntResult = []
    for i in range(0,len(result)-1):
        IntResult.append(int(round(result[i],0)))
    #前沿面中随机选择一个点
    k = random.randint(0,len(IntResult)-1)
    num_fd_list = IntResult[k]
    if num_fd_list >= len(paired_fds):
        num_fd_list = len(paired_fds) - 1
    
    return num_fd_list