#coding=utf-8

from NetworkController import NetworkController

from Init_devide import  *
from CRG import *

class Simulator:
    def __init__(self,positions):
        self.positions = positions
        self.coalition_history = []
        self.fd_history = []
        self.select_history = []


    def simulate(self):

        network = NetworkController(positions)


        initial_divede = Init_devide(network.coalitions, network.fds)

        print "start initial divede"
        initial_divede.random_devide()
        print "start simultan_cus"
        initial_divede.simultan_cus()
        print "finish devide"
        initial_divede.print_devide()

        #初始划分完成，开始进行传输
        max_round = 5
        change_round = 1
        round = 1

        while round <= max_round:
            #每一轮中每个设备按照自己的实际效用来增加效用
            print '\n\n*** round %d' % round
            #保存的是每一个round开始的时候的联盟划分
            network.show_coalitions(round)
            # 1.基站广播每轮中给每个RU传输的数据包数目
            for i in network.coalitions:
                i.ru.N = randint(32, 32)

            # 2.RU与联盟中的FD进行交互,判断哪些设备可以进行中继
            # for i in network.coalitions:
            #     # 在知道了每轮传输的数据包数量之后就可以进行RelaySet和EHSet的更新了
            #     i.get_enough_power_fds()

            # 3.基站广播数据，FD进行能量收集，RU收集信息
            for i in network.coalitions:
                for j in i.EHSet:
                    i.harvestEnergy(j, 0.03125)
                    # i.harvestEnergy(j, i.ru.N / i.bs.rate)

            # 4.FD将自己接收到的信息传输给联盟中的RU,TODO:这里感觉需要实际模拟一下网络编码传输
            for i in network.coalitions:
                for j in i.RelaySet:
                    i.relayMsg(j)



            # 5.RU统计自身还缺失的数据包，向基站发送数据传输请求
            # 6.基站给各个RU广播剩余的数据包 （这个过程还是存在丢包）TODO:这个过程的丢包率过大的话，将需要重复多次才能够结束这个流程
            # 或者直接在下一轮中加入这个需要重传的数据包，还是让中继来一起接收

            #7.结束之后开始调整

            cus = []
            for i in network.coalitions:
                for j in i.fds:
                    if j.total / j.round < j.expect and j.round >= change_round:
                        #这里如果应该先不退出，因为在就餐预测的时候就需要退出了
                        # if j.coalition is not None:
                        #     j.coalition.exit_coa(j)
                        print j.fdId,"join change cus"
                        cus.append(j)
            for i in cus:
                i.search_alternative(network.coalitions)

            #这里什么时候设计成单独的一个类，什么时候设计成一个函数
            network.coalitions = CRG(cus, network.coalitions).sequentialChoose()

            #在进行一轮传输之后，联盟将需要开始更新自己联盟内部的RelaySet和EHset,将RelaySet中不满足的加入到EHSet中，EHSet中满足的加入到RelaySet中

            for i in network.coalitions:
                i.alter_coalition()

            # network.fairness_per_round(round)
            network.gains_per_round(round)
            round += 1

        print "Finish all round"
        network.save_result(max_round)

def random_generate_positions(n_fd, n_ru, x_, _x, y_, _y):
    positions = {
        'RUs':[],
        'FDs':[],
        'BS': [(x_ + _x) / 2, (y_ + _y) / 2]
    }


    for i in range(0, n_fd):
        temp_p = [randint(x_, _x), randint(y_, _y)]
        positions["FDs"].append(temp_p)

    for i in range(0, n_ru):
        temp_p = [randint(x_, _x), randint(y_, _y)]
        positions["RUs"].append(temp_p)

    return positions

if __name__ == '__main__':
    # #这个位置的会出现负数的问题
    # positions = {
    #     'RUs': [[14, 86], [22, 21], [81, 79], [75, 17]],
    #     'FDs': [[16, 48], [87, 62], [20, 91], [26, 14], [24, 63],
    #             [18, 22], [41, 40], [75, 90], [8, 99], [68, 50],
    #             [59, 60], [40, 76], [60, 43], [78, 37], [27, 38],
    #             [63, 14], [63, 81], [75, 75], [55, 31], [61, 90],
    #             [54, 75], [50, 1], [7, 73], [10, 2], [24, 80],
    #             [34, 27], [3, 28], [34, 95], [90, 24], [32, 69]
    #             ],
    #     'BS': [300, 300]
    # }

    positions = {
        'RUs': [[500, 100], [180, 670], [500, 50], [700, 800]],
        'FDs': [
            [38, 823], [8, 929], [94, 356], [924, 477], [150, 610], [833, 33], [394, 71], [468, 446], [578, 202],
            [710, 103] ,
            [432, 622], [113, 705], [553, 73], [627, 751], [514, 307], [569, 225], [594, 67], [229, 812], [57, 526],
            [628, 620] ,
            [566, 880], [483, 205], [17, 663], [442, 505], [319, 582], [62, 402], [560, 244], [116, 909], [239, 867],
            [169, 131] ,
            [35, 577], [491, 16], [472, 74], [397, 284], [369, 715], [920, 341], [137, 825], [212, 853], [54, 158],
            [781, 34],
            [562, 549], [273, 289], [100, 736], [533, 457], [868, 787], [694, 305], [512, 479], [674, 129], [695, 812],
            [639, 836]
            ],
        'BS': [500, 500]
    }

    # positions = random_generate_positions(30, 5, 0, 500, 0, 500)

    s = Simulator(positions)

    s.simulate()
