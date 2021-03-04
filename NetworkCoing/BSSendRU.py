#coding=utf-8
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from FileToMatrix import FToMatrix
from DynamicMultiRelay.LossRate import *
from FDRevBS import FD_Encode
import datetime
import random



def BSSendRU(bs ,ru):
    ori_file = 'NCLog/msg.txt'
    result = FToMatrix(ori_file)
    # 这里先是把文件变成32*32的矩阵，然后对每个矩阵中编号
    num = 0
    matrix = result[num]
    length = len(matrix)

    lr = LossRate_BS(bs, ru)
    # 初始化fd的数据接收集合
    Pkts = {}
    datas = {}  # store data dictionary
    coe_matrix, encode_matrix = [], []
    for i in range(0, length):
        Pkts[i] = False
        datas[i] = ''
    Send_file_dir = 'NCLog/' + str(datetime.date.today()) + '/' + 'BS'
    if os.path.exists(Send_file_dir) != True:
        os.makedirs(Send_file_dir)
    bs_send_cache = Send_file_dir + '/BSSend.txt'
    send_cache = open(bs_send_cache, 'a+')

    Rev_file_dir = 'NCLog/' + str(datetime.date.today()) + '/' + ru.ruId
    if os.path.exists(Rev_file_dir) != True:
        os.makedirs(Rev_file_dir)

    Rev_file_original = Rev_file_dir + '/original_from BS.txt'
    Rev_file_data = Rev_file_dir + '/datas_from_BS.txt'
    Rev_file_coe = Rev_file_dir + '/coe.txt'
    Rev_file_encoded = Rev_file_dir + '/encoded.txt'
    Rev_file_count = Rev_file_dir + '/count_from_BS.txt'
    Rev_file_pkt = Rev_file_dir + '/pkts_from_BS.txt'
    Rev_file_miss = Rev_file_dir + '/miss.txt'
    # 每一个数据包广播所有的设备
    top = 100 * (1 - lr)
    index = 0

    while index < length:
        data = str(matrix[index])
        send_cache.write(data)
        send_cache.write('\n')
        temp = random.randint(0, 100)
        # 写入到目标文件中时还需要统计接收到了哪些数据包,矩阵一行发送一个数据包
        if temp in range(0, top):
            Pkts[index] = True
            datas[index] = data
        index += 1
    send_cache.write('\n')
    send_cache.close()
    # 一轮传输32个包结束之后再开始解码
    # 防止bug产生
    for i in range(len(datas)):
        if datas[i] != '':
            Pkts[i] = True
        else:
            Pkts[i] = False

    true_count = 0

    with open(Rev_file_pkt, 'a+') as f4:
        for i in range(len(Pkts)):
            if Pkts[i] == True:
                f4.write(str(i) + '\n')
                true_count += 1
        f4.write('\n')

    with open(Rev_file_data, 'a+') as f5:
        for i in range(len(datas)):
            if Pkts[i] == True:
                f5.write(datas[i] + '\n')
        f5.write('\n')

    with open(Rev_file_count, 'a+') as f6:
        f6.write(str(true_count) + '\n')