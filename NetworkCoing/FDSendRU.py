#coding=utf-8

import datetime
import os,sys
from decode import solve



total = 32
size = 32
Pkts = {}  #Pkts from DU
coe = {}   #store coe matrix dictionary
enc = {}
coe_DU = []  #保存来自DU的系数矩阵
enc_DU = []  #保存来自DU的编码数组

#pretreatment
for i in range(total):
    Pkts[i] = False
    coe[i] = []
    enc[i] = []





def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    return [int(i) for i in s.split(',')]


def FDSendRU(fd, ru):
    pkts = {}
    datas = {}  # data receive from AP
    for i in range(size):
        pkts[i] = False
        datas[i] = ''


    file_dir = 'NCLog/'+str(datetime.date.today())+'/' + fd.fdId

    file_coe = file_dir + "/coe.txt" #1
    file_encoded = file_dir + "/encoded.txt" #2
    file_count = file_dir + "/count.txt" #3
    file_pkt= file_dir + "/pkts.txt" #4

    index = 0
    with open(file_count, 'r') as f3:
        buffer3 = f3.readlines()
        lenth = int(buffer3[-1])
        print('length', lenth)
    with open(file_pkt, 'r') as f4:
        buffer4 = f4.readlines()
    pkt_start = len(buffer4) - (lenth + 1)
    for i in range(lenth):
        index = int(buffer4[pkt_start + i])
        pkts[index] = True
    f1 = open(file_coe, 'r')
    f2 = open(file_encoded, 'r')
    buffer1 = f1.readlines()
    buffer2 = f2.readlines()
    coe_start = len(buffer1) - (lenth + 1)
    encode_start = len(buffer2) - (lenth + 1)
    # print('pkts', pkts)
    # print('coe', buffer1[coe_start])
    i = 0  # 由于系数矩阵的文件是没有空的
    for index in range(size):
        if pkts[index] == True:
            # time.sleep(0.5)
            coe = buffer1[coe_start + i][:-1]  # take out '\n'
            enc = buffer2[encode_start + i][:-1]
            # data_send = ''.join(data)
            # print('index', index)
            # print('coe', coe)
            # print('enc', enc)
            #原本发送的时候是将系数矩阵和编码之后的数据包一起发送的
            # msg = "send_time: " + "%.6f" % float(now) + "total:%d" % size + "index:%d" % index + "coe:" + coe + "enc:" + enc
            i += 1
        # send的过程改成文件读写


    f1.close()
    f2.close()

#读取之间AP给RU发送的文件
def readAPtoRU(ru, pkts_AP, datas_AP):

    file_dir = 'NCLog/' + str(datetime.date.today()) + '/' + ru.ruId
    filename1 = file_dir + '/count_from_BS.txt'
    filename2 = file_dir + '/pkts_from_BS.txt'
    filename3 = file_dir + '/datas_from_BS.txt'
    with open(filename1, 'r') as f1:
        buffer1 = f1.readlines()
        length = int(buffer1[-1])
        print('BS_length', length)
    with open(filename2, 'r') as f2:
        buffer2 = f2.readlines()
    with open(filename3, 'r') as f3:
        buffer3 = f3.readlines()
    pkt_start = len(buffer2) - (length + 1)
    data_start = len(buffer3) - (length + 1)
    # print(buffer2[pkt_start:])
    # print(buffer3[data_start:])
    for i in range(length):
        index = int(buffer2[pkt_start + i])
        pkts_AP[index] = True
        vector = stringToList(buffer3[data_start + i][0:-1])  # take out '\n'
        # print(vector)
        datas_AP[index] = vector

#将矩阵转化为列
def GetMatrixCol(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for j in range(cols):
        result.append([matrix[i][j] for i in range(rows)])
    return result

def BuildMatrix(fd, pkts_AP, datas_AP):
    #参数：pkts_AP & datas_AP ：建立稀疏矩阵    coe_DU & enc_DU : 建立增广矩阵   Pkts ：确定填充的位置，是不是应该根据DU的pkt确定？

    #
    coe_matrix = []  #总的系数矩阵
    encoded_matrix = []  #总的编码矩阵

    #解码DU的pkt
    #这里需要传入FD的设备编号，读取的是FD的数据
    fd_rev_dir = 'NCLog/' + str(datetime.date.today()) + '/' + fd.fdId
    filename1 = "/pkts.txt"
    filename2 = "/count.txt"
    with open(filename2, 'r') as f2:
        buffer2 = f2.readlines()
        FD_length = int(buffer2[-1])
    with open(filename1, 'r') as f1:
        buffer = f1.readlines()
    pkt_start = len(buffer) - (FD_length + 1)
    DU_pkt = {}
    for i in range(size):
        DU_pkt[i] = False
    for i in range(FD_length):
        index = int(buffer[pkt_start + i])
        DU_pkt[index] = True

    # 从AP收到的包的矩阵
    for i in range(len(pkts_AP)):
        if pkts_AP[i] == True:
            coe_vector = [0] * size
            coe_vector[i] = 1
            enc_vector = datas_AP[i]
            coe_matrix.append(coe_vector)
            encoded_matrix.append(enc_vector)
    print('coe:', coe_matrix)
    print('enc:', encoded_matrix)
    #建立增广矩阵
    augment_matrix = [([0] * size) for i in range(len(coe_DU))]        #len(coe_DU) * size
    #coe_cols = GetMatrixCol(coe_DU)
    index = 0  # 指向列的指针

    #判断DU_pkt来确定那一列缺失，如果RU丢包，那么只是行缺失
    for j in range(len(DU_pkt)):
        if DU_pkt[j] == True:
            for i in range(len(augment_matrix)):
                augment_matrix[i][j] = coe_DU[i][index]
            index += 1
    coe_matrix.extend(augment_matrix)
    encoded_matrix.extend(enc_DU)
    print('coe_matrix', coe_matrix)
    print('encoded_matrix', encoded_matrix)
    return coe_matrix, encoded_matrix

def RU_decode(ru):

    ru_rev_dir = 'NCLog/' + str(datetime.date.today) + '/' + ru.ruId
    filename4 = ru_rev_dir + "/RU_pkts.txt"
    with open(filename4, 'a+') as f4:
        f4.write(str(Pkts) + '\n')

    filename5 = ru_rev_dir + "/RU_datas.txt"
    with open(filename5, 'a+') as f5:
        f5.write('RU receive from DU coefficient matrix:\n')
        f5.write(str(coe) + '\n')
        f5.write('RU receive from DU encoded matrix:\n')
        f5.write(str(enc) + '\n')

    print("RU begin Decode>>>>>>>>>")
    #读取之前AP给RU发送的信息，并且保存
    pkts_AP = {}
    datas_AP = {}
    for i in range(size):
        pkts_AP[i] = False
        datas_AP[i] = []
    readAPtoRU(ru, pkts_AP, datas_AP)
    print('pkts_AP', pkts_AP)
    print('datas_AP', datas_AP)
    #根据两次收到的信息建立系数和编码矩阵
    # 改造之后就不需要查找fd的
    coe_matrix, encoded_matrix = BuildMatrix(ru,  pkts_AP, datas_AP)

    #对每一列进行解码
    #将编码矩阵转化为一列一列的向量。
    encoded_cols = GetMatrixCol(encoded_matrix)
    original_matrix = []   #解码出来的原始数据存放
    for i in range(len(encoded_cols)):
        sigma, res = solve(coe_matrix, encoded_cols[i])
        original_matrix.append(res)
    print('original', original_matrix)

    #检测是不是有没有解码到的，需要重传，例如x_5没有解码到的话会返回x_5(free val)
    #只需要检测第一行
    miss_pkt = []
    for i in range(len(original_matrix[0])):
        if original_matrix[0][i][-4:-1] == 'var':
            for j in range(len(original_matrix)):
                original_matrix[j][i] = '-1'   #将不能解码的元素变为-1
            miss_pkt.append(i)
    print('miss_pkt', miss_pkt)
    filename7 = ru_rev_dir + "/miss.txt"
    with open(filename7, 'a+') as f7:
        if miss_pkt == []:
            f7.write('ACK')
            f7.write('\n')
        else:
            f7.write(str(miss_pkt))
            f7.write('\n')

    #将original写在文件里面
    filename9 = ru_rev_dir +"/RU_original.txt"
    for i in range(len(original_matrix)):
        for j in range(len(original_matrix[0])):
            original_matrix[i][j] = int(original_matrix[i][j])
    with open(filename9, 'a+') as f9:
        for item in original_matrix:
            f9.write(str(item) + '\n')
        f9.write('\n')