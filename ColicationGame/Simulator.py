# coding=utf-8

import random
import matplotlib.pyplot as plt
# from mininet.log import setLogLevel, info

from NetworkController import NetworkController
from CoalitionGame import CoalitionGame
from StackelbergGame import StackelbergGame
import NetworkEnvironment as ne
import Drawer as d


class Simulator:
    def __init__(self, positions):
        self.positions = positions
        self.coalition_history = []
        self.fd_history = []
        self.select_history = []

        self.network = None

    def simulate(self):
        network = NetworkController(positions)
        network.start_net()

        coalition_game = CoalitionGame(network.coalitions, network.fds)
        stackelberg_game = StackelbergGame(network.coalitions, network.fds)

        # 初始化联盟
        print '*** initial games\n'
        coalition_game.init_coalitions()
        stackelberg_game.init_game()

        print '*** start game\n'
        print '\n\ninitial info:'
        network.show_coalitions(0)
        # network.show_fds()

        max_round = 20
        cfg_round_per_round = 5
        round = 0
        while round < max_round:
            print '\n\n*** round %d' % round
            for _ in range(cfg_round_per_round):
                network.start_game(coalition_game, round, max_round)
            network.start_game(stackelberg_game, round, max_round)
            for coalition in network.coalitions:
                # sel_fd = coalition.select_fd()
                sel_fd = coalition.select_fd_with_fairness()

                # ap broadcast and fd harvest energy
                for fd in coalition.paired_fds:
                    if fd != sel_fd:
                        fd.harvest_energy(coalition.bs, 0.03125)
                # transmission
                if sel_fd is not None:
                    print 'fd %2d in coalition %d was selected to forward' % (sel_fd.num, coalition.num)
                    sel_fd.forward_data()
                else:
                    # 如果所有中继设备能量都不够，则基站自己传输
                    print 'None is selected in coalition %d' % coalition.num
            # self.save_select(network)
            network.show_coalitions(round)
            network.gains_per_round(round)
            round += 1


        network.save_result(max_round)

            # network.show_fds()
            # self.save_coalition(network)

        # 开始发送信息
        # total_round = 30  # 时间大小
        # for _ in range(total_round):
        #     for coalition in network.coalitions:
        #         sel_fd = coalition.select_fd()
        #         # sel_fd = coalition.select_fd_with_fairness()
        #         # ap broadcast and fd harvest energy
        #         for fd in coalition.paired_fds:
        #             if fd != sel_fd:
        #                 fd.harvest_energy(coalition.bs, 0.03125 / total_round)
        #         # transmission
        #         if sel_fd is not None:
        #             print 'fd %2d in coalition %d was selected to forward' % (sel_fd.num, coalition.num)
        #             sel_fd.forward_data()
        #         else:
        #             # 如果所有中继设备能量都不够，则基站自己传输
        #             print 'None is selected in coalition %d' % coalition.num
        #     self.save_select(network)

        print '*** end simulate\n'
        # self.save_history_file()

    def save_select(self, network):
        c_his = []
        for c in network.coalitions:
            fd = c.selected_fd
            sel_his = {}
            if fd != None:
                sel_his['num'] = fd.num
                sel_his['f_bs'] = fd.f_bs
                sel_his['f_fd'] = fd.f_fd
                sel_his['gains'] = fd.gains
                sel_his['power'] = fd.power
            c_his.append(sel_his)
        self.select_history.append(c_his)

    # def save_history(self, network):
    #     self.save_coalition(network)
    #     self.save_fd(network)

    def save_coalition(self, network):
        cs = []
        for c in network.coalitions:
            c_his = {}
            c_his['paired_fds'] = [fd.num for fd in c.paired_fds]
            # c_his['fairness'] = ne.cal_fairness(c.paired_fds)
            # c_his['capacity'] = ne.get_coalition_capacity(c)
            c_his['capacity'] = ne.swap_coalition_capacity(c)
            c_his['game_sel'] = c.selected_fd.num
            c_his['num'] = c.num
            # c_his['selected_fd'] = c.selected_fd.num
            cs.append(c_his)

        #这里把每次的联盟划分记录下来
        self.coalition_history.append(cs)

    def save_fd(self, network):
        fds = []
        for fd in network.fds:
            fd_his = {}
            fd_his['power'] = fd.power
            if fd.coalition is not None:
                fd_his['coalition'] = fd.coalition.num
            fd_his['gains'] = fd.gains
            fd_his['N1'] = fd.N1
            fd_his['N'] = fd.N
            fd_his['f_bs'] = fd.f_bs
            fd_his['f_fd'] = fd.f_fd
            fd_his['loss_rate'] = fd.loss_rate

            fds.append(fd_his)

        self.fd_history.append(fds)
            
    def show_topology(self):
        bs = self.positions['BS']
        rus = self.positions['rus']
        fds = self.positions['fds']
        plt.scatter(bs[0], bs[1], marker='^', c='b', s=100)
        plt.text(bs[0], bs[1], 'BS')
        plt.scatter([x[0] for x in rus], [y[1] for y in rus], marker='o', c='g', s=80)
        plt.scatter([x[0] for x in fds], [y[1] for y in fds], marker='o', c='r')
        for i in range(len(rus)):
            plt.text(rus[i][0], rus[i][1], 'RU %d' % i)
        for i in range(len(fds)):
            plt.text(fds[i][0], fds[i][1], 'FD %2d' % i)
        plt.show()

    def show_capacity(self):
        y1s = [ c[0]['capacity'] for c in self.coalition_history ]
        y2s = [ c[1]['capacity'] for c in self.coalition_history ]
        y3s = [ c[2]['capacity'] for c in self.coalition_history ]
        y4s = [ c[3]['capacity'] for c in self.coalition_history ]
        xs = range(1, 4)

        plt.plot(xs, y1s, c='r')
        plt.plot(xs, y2s, c='y')
        plt.plot(xs, y3s, c='b')
        plt.plot(xs, y4s, c='g')

        plt.show()

    def print_sum_capacity(self):
        l_c = []
        for r in self.coalition_history:
            capacity = 0.0
            for c in r:
                capacity += c['capacity']
            l_c.append(capacity)
        print 'capacity history: ', l_c

    def print_fd_power(self):
        for i in range(len(self.fd_history[0])):
            fd_powers = []
            for r in self.fd_history:
                fd_powers.append(r[i]['power'])
            print 'fd %2d power: ' % i, fd_powers

    def print_fd_f_bs(self):
        f_his = []
        for r in self.coalition_history:
            f_bs_sum = 0.0
            for c in r:
                f_bs_sum += c['f_bs']
            f_his.append(f_bs_sum)
        print 'f_bs_his: ', f_his
        # print 'net.save_f: ', self.f_history


def random_position(size, fd_num, ru_num):
    positions = {'BS': [size / 2, size / 2, 0]}
    fds = []
    for i in range(fd_num):
        fds.append([random.randint(70, 80), random.randint(70, 80), 0])
    positions['fds'] = fds
    rus = []
    for i in range(ru_num):
        rus.append([random.randint(70, 85), random.randint(70, 85), 0])
    positions['rus'] = rus
    print positions
    return positions


if __name__ == '__main__':
    # positions = random_position(100, 30, 4)
    positions = {
        'rus': [[14, 86, 0], [22, 21, 0], [81, 79, 0], [75, 17, 0]],
        'fds': [[16, 48, 0], [87, 62, 0], [20, 91, 0], [26, 14, 0], [24, 63, 0],
                [18, 22, 0], [41, 40, 0], [75, 90, 0], [8, 99, 0], [68, 50, 0],
                [59, 60, 0], [40, 76, 0], [60, 43, 0], [78, 37, 0], [27, 38, 0],
                [63, 14, 0], [63, 81, 0], [75, 75, 0], [55, 31, 0], [61, 90, 0],
                [54, 75, 0], [50, 1, 0], [7, 73, 0], [10, 2, 0], [24, 80, 0],
                [34, 27, 0], [3, 28, 0], [34, 95, 0], [90, 24, 0], [32, 69, 0]],
        'BS': [50, 50, 0]}

    # positions = {
    #     'rus': [[50, 50, 0], [50, 10, 0]],
    #     'fds': [[25, 53, 0], [30, 42, 0], [35, 35, 0], [20, 25, 0], [15,10, 0]],
    #     'BS': [5, 45, 0]
    # }
    # positions = {
    #     'RUs': [[50, 50], [50, 10]],
    #     'FDs': [[25, 53], [30, 42], [35, 35], [20, 25], [15,10]],
    #     'BS': [5, 45]
    # }
    #setLogLevel('info')
    s = Simulator(positions)
    # s.show_topology()
    s.simulate()
    # s.print_fd_power()
    # s.print_sum_capacity()
    # s.print_fd_f_bs()
    # s.show_capacity()

    # d.draw_f_bs(s.coalition_history)

    print '\n\n***********************'
    print 'coalition_history = ', s.coalition_history
    print '***********************'
    print 'select_history = ', s.select_history