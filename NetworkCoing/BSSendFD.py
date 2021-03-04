#coding=utf-8
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from FileToMatrix import FToMatrix
from DynamicMultiRelay.LossRate import *
from FDRevBS import FD_Encode
import datetime
import random

def BSSendFD(bs, fd):
    ori_file = 'NCLog/msg.txt'
    result = FToMatrix(ori_file)
    #这里先是把文件变成32*32的矩阵，然后对每个矩阵中编号
    num = 0
    matrix = result[num]
    length = len(matrix)

    lr = LossRate_BS(bs, fd)
    #初始化fd的数据接收集合
    Pkts = {}
    datas = {}  # store data dictionary
    coe_matrix, encode_matrix = [], []
    for i in range(0,length):
        Pkts[i] = False
        datas[i] = ''

    Rev_file_dir = 'NCLog/'+str(datetime.date.today())+'/' + fd.fdId
    if os.path.exists(Rev_file_dir) != True:
        os.makedirs(Rev_file_dir)

    Rev_file_data = Rev_file_dir + '/datas.txt'
    Rev_file_coe = Rev_file_dir + '/coe.txt'
    Rev_file_encoded = Rev_file_dir + '/encoded.txt'
    Rev_file_count = Rev_file_dir + '/count.txt'
    Rev_file_pkt = Rev_file_dir + '/pkts.txt'

    #每一个数据包广播所有的设备
    top = 100 * (1 - lr)

    index = 0


    while index < length:
        data = str(matrix[index])
        temp = random.randint(0,100)
        # 写入到目标文件中时还需要统计接收到了哪些数据包,矩阵一行发送一个数据包
        if temp in range(0, top):
            Pkts[index] = True
            datas[index] = data
        index += 1

    #一轮传输32个包结束之后再开始解码
    #防止bug产生
    for i in range(len(datas)):
        if datas[i] != '':
            Pkts[i] = True
        else:
            Pkts[i] = False

    with open(Rev_file_pkt, 'a+') as f4:
        for i in range(len(Pkts)):
            if Pkts[i] == True:
                f4.write(str(i) + '\n')
        f4.write('\n')

    with open(Rev_file_data, 'a+') as f5:
        f5.write(str(datas) + '\n')

    print('Encoding>>>>>>>>>>>>>')
    # 这里DU接收到的是原始数据，重新进行编码
    coe_matrix, encode_matrix = FD_Encode(Pkts, datas, size)

    with open(Rev_file_coe, 'a+') as f6:
        for item in coe_matrix:
            f6.write(str(item) + '\n')
        f6.write('\n')

    with open(Rev_file_encoded, 'a+') as f7:
        for item in encode_matrix:
            f7.write(str(item) + '\n')
        f7.write('\n')

    count = 0
    for i in range(len(Pkts)):
        if Pkts[i] == True:
            count += 1
    with open(Rev_file_count, 'a+') as f8:
        f8.write(str(count) + '\n')

    print('Encode finish')