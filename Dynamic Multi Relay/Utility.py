#coding=utf-8

from LossRate import *

def solidInfo(bs, fd, ru, set):
    e1 = LossRate_FDS_RU(bs, ru)
    l = 1

    for i in ru.getset(set):
        l *= LossRate_BS(bs, i)

    l *= LossRate_BS(bs, fd)
    if l == 1:
        return ru.N * e1
    else:
        return ru.N * e1 * (1 - l)

def utility(bs, fd, ru, set):
    #这里是没有BS实例的
    w_fd = (1 - LossRate_FDS_RU(bs, fd)) * (1 - LossRate_FDS_RU(fd, ru))
    w_total = 0.0
    for i in ru.getset(set):
        #TODO:这里到底要不要乘后面从FD到RU的链路丢包率，也就是有效信息量的定义问题
        w_total += (1 - LossRate_FDS_RU(i, bs)) * (1 - LossRate_FDS_RU(i, ru))
    if fd.choice != ru.ruId:
        w_total += w_fd
    #这里的有效信息计算有问题，应该是算加入之后的
    n = int(w_fd / w_total * solidInfo(bs, fd, ru, 0))
    return n


