#coding=utf-8
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from DynamicMultiRelay.FogDevice import FD
from DynamicMultiRelay.RegisterUser import RU
from DynamicMultiRelay.BaseStation import BS
from BSSendFD import BSSendFD
from BSSendRU import BSSendRU
from FDSendRU import FDSendRU
from FDSendRU import RU_decode
# 这个文件设计对比试验，验证需要满足RU接收到所有文件需要的传输轮次
total = 32
size = 32


if __name__ == '__main__':

    #创建设备
    bs = BS([100, 100])
    FD1 = FD('FD1',[200, 300])
    FD2 = FD('FD2',[250, 350])
    FD3 = FD('FD3',[300, 350])
    fds = [FD1, FD2, FD3]
    ru1 = RU('RU1', [600, 600])
    #1.基站广播
    for i in fds:
        BSSendFD(bs, i)
    BSSendRU(bs, ru1)
    #2.FD将自身数据包发送给RU
    for i in fds:
        FDSendRU(i, ru1)
    #3.RU从各个数据包里面开始解码
    # TODO:如果解码需要FD的pkts,那么如何使用多个FD发送过来的数据包进行解码，感觉需要对解码过程改造
    # 方案一：计算一下所有的FD接收到所有数据包的概率，如果这个概率比较大，那么就可以直接认为是一个拥有所有数据包的FD发送过来的数据吧
    for i in fds:
        RU_decode(i,ru1)

    #4.RU统计自身的信息

