import math
import random
from sympy import *

from StackelbergGame import fds_game as fg

def get_receive_power(sender, receiver):
    p_receiver = receiver.position
    p_sender = sender.position
    l = math.sqrt((p_receiver[0] - p_sender[0]) ** 2 + (p_receiver[1] - p_sender[1]) ** 2)
    if sender == receiver:
        l = 10.0
    return sender.P_T + sender.G_T + sender.G_R + 20 * math.log(3.0 * 10 ** 8 / (sender.W * 4.0 * math.pi * l), 10)

def get_coalition_capacity(coalition):
    bs = coalition.bs
    total_capacity = 0.0
    fd = coalition.selected_fd
    if fd != None:
    # for fd in coalition.paired_fds:
        sel_p = get_receive_power(bs, coalition) + get_receive_power(fd, coalition)
        sel_i = coalition.N
        for fd_k in coalition.paired_fds:
            if fd_k != fd:
                sel_i += get_receive_power(fd_k, coalition)
        sel_fd_capacity = math.log(sel_p / sel_i + 1, 2)

        unsel_fd_capacity = 0.0
        for fd_j in coalition.paired_fds:
            if fd_j != fd:
                unsel_p = get_receive_power(fd, fd)
                unsel_i = coalition.N
                for fd_k in coalition.paired_fds:
                    if fd_k != fd:
                        if fd_k != fd_j:
                            unsel_i += get_receive_power(fd_k, fd_j)
                    else:
                        unsel_i += get_receive_power(coalition, fd_j)
                unsel_fd_capacity += math.log(unsel_p / unsel_i + 1)
        
        total_capacity += sel_fd_capacity + unsel_fd_capacity

    return total_capacity

def swap_coalition_capacity(coalition):
    bs = coalition.bs
    i = coalition.N
    for fd in coalition.paired_fds:
        i += get_receive_power(fd, coalition.ru)
    capacity = 0.0
    for fd in coalition.paired_fds:
        p = get_receive_power(bs, fd) + get_receive_power(fd, coalition.ru)
        capacity += math.log( p / (i-p) + 1, 2)
    
    return capacity

def power_coalition_capacity(coalition):
    p = 0.0
    for fd in coalition.paired_fds:
        p += get_receive_power(fd, coalition)
    return p

def f_bs_coalition(coalition):
    total_f_bs = 0.0
    for fd in coalition.paired_fds:
        fd.N1, fd.b, fd.f_bs, fd.f_fd = fg(1.0-fd.loss_rate)
        total_f_bs += fd.f_bs
    return total_f_bs

def get_total_f_bs(coalition):
    total_f_bs = 0.0
    for fd in coalition.paired_fds:
        total_f_bs += fd.f_bs
    return total_f_bs

def need_swap(fd_a, fd_b, round, max_round):
    before_capacity = swap_coalition_capacity(fd_a.coalition) + swap_coalition_capacity(fd_b.coalition)
    # before_capacity = get_coalition_capacity(fd_a.coalition) + get_coalition_capacity(fd_b.coalition)
    # before_capacity = power_coalition_capacity(fd_a.coalition) + power_coalition_capacity(fd_b.coalition)
    # before_capacity = fd_a.f_bs + fd_b.f_bs

    fd_a.swap(fd_b)

    after_capacity = swap_coalition_capacity(fd_a.coalition) + swap_coalition_capacity(fd_b.coalition)
    # after_capacity = get_coalition_capacity(fd_a.coalition) + get_coalition_capacity(fd_b.coalition)
    # after_capacity = power_coalition_capacity(fd_a.coalition) + power_coalition_capacity(fd_b.coalition)
    # after_capacity = fg(1.0-fd_a.loss_rate) + fg(1.0-fd_b.loss_rate)

    # reset environment
    fd_a.swap(fd_b)

    if before_capacity < after_capacity:
        return True
    else:
        return False
        # beta = random.uniform(0, 1)
        # passible = ((after_capacity - before_capacity) / before_capacity) * (1 - round / max_round)
        # if beta < passible:
        #     print '    beta, passible: %f, %f' % (beta, passible)  
        #     return True
        # else:
        #     return False

def cal_fairness(fds):
    U_total = 0
    U_link_s = 0
    for i in range(0,len(fds)):
        U_total += fds[i].gains
        U_link_s += (1-fds[i].loss_rate)
    X=[]
    for i in range(0,len(fds)):
        Ui_overline = ((1-fds[i].loss_rate)/U_link_s)*U_total
        if fds[i].gains <= Ui_overline:
            X.append(fds[i].gains/Ui_overline)
        else:
            X.append(1.0)
    sum_of_xi = 0
    for i in range(0,len(X)):
        sum_of_xi += X[i]

    sum_of_xi2 = 0
    for i in range(0,len(X)):
        sum_of_xi2 += X[i]**2

    fairness = (sum_of_xi)**2/(len(X)*sum_of_xi2)
    return fairness

def get_loss_rate(fd, coalition):
    FDPosition = fd.host.params['position'][0:2]
    RUPosition = coalition.host.params['position'][0:2]
    distance = math.sqrt((FDPosition[0] - RUPosition[0]) ** 2 + (FDPosition[1] - RUPosition[1]) ** 2)

    y = Symbol('y')
    a = 3.0
    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (2.0 / a - 1) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2.0 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
    nk = 1.0 ** (2.0 / a)
    nk = nk * 5.0 / (10.0 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    PLR = round(1 - BSR ** 1024, 6)
    return PLR

def cal_loss_rate(fd):
    FDPosition = fd.position
    RUPosition = fd.coalition.ru.position
    distance = math.sqrt((FDPosition[0] - RUPosition[0]) ** 2 + (FDPosition[1] - RUPosition[1]) ** 2)

    y = Symbol('y')
    a = 3.0
    f1 = y ** (2.0 / a - 1) * exp(-y)
    f2 = y ** (2.0 / a - 1) * exp(-y)
    I1 = integrate(f1, (y, 0, oo))
    I2 = integrate(f2, (y, 0, oo))
    Ca = (2.0 * pi / a) * I1 * I2
    ek = Ca * (distance ** 2.0) * (3.0 ** (2.0 / a))
    nk = 1.0 ** (2.0 / a)
    nk = nk * 5.0 / (10.0 ** 8)
    ek = ek * nk
    BSR = exp(-ek)
    PLR = round(1 - BSR ** 1024, 6)
    return PLR