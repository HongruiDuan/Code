# coding=utf-8

import math
import NetworkEnvironment as ne

class Coalition:
    # todo: check the default value
    def __init__(self, ru, num, W=2500000000.0, N=1.0, P_T=6.0206, G_T=0.0, G_R=0.0):
        # 用户设备 host
        self.ru = ru

        # 设备编号
        self.num = num

        # 附近的中继设备 FD
        self.nearby_fds = []

        # 参加联盟的中继设备 FD
        self.paired_fds = []

        self.selected_fd = None

        # 高斯白噪声
        self.P_T = P_T
        self.G_R = G_R
        self.G_T = G_T
        self.W = W
        self.N = N

    def could_swap_fds(self, coalition):
        nearby_fds = set(self.nearby_fds) & set(coalition.nearby_fds)
        return list(set(self.paired_fds) & nearby_fds), list(set(coalition.paired_fds) & nearby_fds)

    def disconnect(self, fd):
        for i in range(len(self.paired_fds)):
            if self.paired_fds[i] == fd:
                fd.coalition = None
                del self.paired_fds[i]
                break

    '''
    select an fd in coalition
    return none while there has no passible fd
    '''
    def select_fd(self):
        fd_list = self.get_enough_power_fds()
        
        if len(fd_list) < 1:
            self.selected_fd = None
            return None
        
        selected_fd = fd_list[0]

        for fd in fd_list:
            if selected_fd.f_bs < fd.f_bs:
                selected_fd = fd

        self.selected_fd = selected_fd
        return selected_fd

    def select_fd_with_fairness(self):
        fd_list = self.get_enough_power_fds()

        if len(fd_list) < 1:
            self.selected_fd = None
            return None

        num = self.rank(fd_list)
        if num == -1:
            return self.select_fd()

        return fd_list[num]

    def rank(self, fd_list):
        total_gains = 0.0
        total_gain_rate = 0.0
        for fd in fd_list:
            total_gains += fd.gains
            total_gain_rate += 1-fd.loss_rate
        if (total_gains < 1.0):
            return -1
        
        fairness = []
        for i in range(len(fd_list)):
            fd_overline = (1-fd_list[i].loss_rate) / total_gain_rate * total_gains
            if fd_list[i].gains <= fd_overline:
                fairness.append(fd_list[i].gains / fd_overline)
            else:
                fairness.append(1.0)
        
        score = [(1-fairness[i])*fd_list[i].f_bs for i in range(len(fd_list))]
        max_score = score[0]
        max_num = 0
        for i in range(len(fd_list)):
            if score[i] > max_score:
                max_num = i
        return max_num
        

    def get_enough_power_fds(self):
        l = []
        for fd in self.paired_fds:
            if fd.N1*0.00004 < fd.power:
                l.append(fd)
        return l