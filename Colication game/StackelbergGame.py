# coding=utf-8
from sympy import Symbol, solve
from math import log
import random


class StackelbergGame:
    def __init__(self, coalitions, fds):
        self.fds = fds
        self.coalitions = coalitions

    def init_game(self):
        for c in self.coalitions:
            for fd in c.paired_fds:
                fd.N1, fd.b, fd.f_bs, fd.f_fd = self.game(1.0-fd.loss_rate)
            c.select_fd()

    def start(self, round, max_round):
        for c in self.coalitions:
            for fd in c.paired_fds:
                fd.N1, fd.b, fd.f_bs, fd.f_fd = self.game(1.0-fd.loss_rate)
            c.select_fd()

    '''
    S       # 丢包率
    C       # RU对包的基本支付单价
    C_DU    # DU传输一个包的成本
    C_BS    # BS传输一个包的成本
    N       #总包数
    a       # 满足因子
    '''

    def game(self, S, C=3, C_DU=2, C_BS=1, N=32, a=2):
        x = Symbol('x')
        # expr1 = x*(C_BS+(C*N*S)/(log(a)*(a+S*x)))
        expr1 = C_BS + C * N * S / (log(a) * (a + S * x)) + \
            x * (-C * N * S * S) / (log(2) * (a + S * x) * (a + S * x)) - C_DU
        # N1 = solve(diff(expr1,x),x)

        ans = solve(expr1, x)

        N1 = ans[0]
        for i in range(0, len(ans)):
            if ans[i] > 0:
                N1 = ans[i]

        temp = int(N1)
        U_L = temp * (C_BS + C * N * S / (log(a) * (a + S * temp))) - C_DU * temp  # 向下取整的时候的效益
        temp = temp + 1
        U_H = temp * (C_BS + C * N * S / (log(a) * (a + S * temp))) - C_DU * temp  # 向上取整的时候的效益
        if U_L > U_H:
            N1 = temp - 1
            U_DU = U_L
        else:
            N1 = temp
            U_DU = U_H
        b = C_BS + C * N * S / (log(a) * (a + S * N1))
        U_BS = C * N * log(a + S * N1, a) - b * N1 - (N - N1) * C_BS

        return N1, b, U_BS, U_DU

def fds_game(S, C=3, C_DU=2, C_BS=1, N=32, a=2):
    x = Symbol('x')
    # expr1 = x*(C_BS+(C*N*S)/(log(a)*(a+S*x)))
    expr1 = C_BS + C * N * S / (log(a) * (a + S * x)) + \
        x * (-C * N * S * S) / (log(2) * (a + S * x) * (a + S * x)) - C_DU
    # N1 = solve(diff(expr1,x),x)

    ans = solve(expr1, x)

    N1 = ans[0]
    for i in range(0, len(ans)):
        if ans[i] > 0:
            N1 = ans[i]

    temp = int(N1)
    U_L = temp * (C_BS + C * N * S / (log(a) * (a + S * temp))) - C_DU * temp  # 向下取整的时候的效益
    temp = temp + 1
    U_H = temp * (C_BS + C * N * S / (log(a) * (a + S * temp))) - C_DU * temp  # 向上取整的时候的效益
    if U_L > U_H:
        N1 = temp - 1
        U_DU = U_L
    else:
        N1 = temp
        U_DU = U_H
    b = C_BS + C * N * S / (log(a) * (a + S * N1))
    U_BS = C * N * log(a + S * N1, a) - b * N1 - (N - N1) * C_BS

    return N1, b, U_BS, U_DU