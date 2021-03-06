#coding=utf-8

import GF
import random

w = 8
total = 2 ** w
gf = GF.GF(w)

def vector_mul(a, b):
    res = 0
    for i in range(len(a)):
        res = gf.add(res, gf.mul(a[i], b[i]))
    return res

def matrix_mul(a, b):
    a_row = len(a)
    b_col = len(b[0])
    b_row = len(b)
    result = []
    for i in range(a_row):
        row_vector = []
        for j in range(b_col):
            row_vector.append(vector_mul(a[i], [b[m][j] for m in range(b_row)]))
        result.append(row_vector)
    return result

def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    #print(s)
    return [int(i) for i in s.split(',')]


def FD_Encode(pkts, datas, size):
    count = 0
    data_matrix = []
    for i in range(len(pkts)):
        if pkts[i] == True:
            count += 1
            data_matrix.append(stringToList(datas[i]))
    coe_matrix = [([0] * count) for i in range(size)]    # size * count
    for i in range(size):
        for j in range(count):
            coe_matrix[i][j] = random.randint(1, 2 ** w - 1)
    encode_matrix = matrix_mul(coe_matrix, data_matrix)
    # print('coe', coe_matrix)
    # print('data', data_matrix)
    # print('encode', encode_matrix)
    return coe_matrix, encode_matrix

#Unit test
# pkts = {0: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True, 17: True, 18: True, 19: True, 20: True, 21: True, 22: True, 23: True, 24: True, 25: True, 26: True, 27: True, 28: True, 29: True, 30: True, 31: True}
# datas = {0: '[32, 101, 98, 32, 46, 108, 116, 101, 32, 117, 121, 115, 111, 111, 32, 101, 101, 98, 104, 103, 32, 99, 97, 111, 104, 105, 32, 97, 111, 115, 111, 32]', 1: '[32, 32, 117, 115, 32, 112, 111, 114, 116, 108, 44, 101, 110, 110, 102, 110, 121, 101, 101, 32, 119, 99, 103, 108, 97, 115, 116, 108, 112, 46, 114, 105]', 2: '[87, 101, 115, 111, 76, 115, 109, 115, 104, 116, 32, 32, 111, 101, 111, 32, 32, 99, 32, 67, 104, 101, 101, 100, 110, 32, 104, 115, 108, 32, 121, 115]', 3: '[105, 99, 105, 32, 101, 32, 101, 32, 101, 32, 116, 108, 117, 115, 114, 116, 99, 97, 115, 104, 105, 110, 32, 32, 32, 98, 101, 111, 101, 87, 32, 32]', 4: '[116, 111, 110, 97, 97, 116, 114, 115, 121, 108, 104, 97, 110, 32, 101, 104, 97, 117, 97, 105, 99, 116, 105, 112, 102, 105, 32, 32, 44, 101, 98, 116]', 5: '[104, 110, 101, 115, 114, 104, 115, 116, 32, 97, 101, 110, 99, 104, 105, 101, 110, 115, 109, 110, 104, 46, 115, 111, 105, 103, 115, 100, 32, 32, 121, 104]', 6: '[32, 111, 115, 32, 110, 101, 44, 97, 102, 110, 114, 103, 101, 97, 103, 121, 32, 101, 101, 101, 32, 10, 32, 101, 118, 32, 97, 105, 108, 99, 32, 101]', 7: '[116, 109, 115, 116, 105, 109, 32, 114, 105, 103, 101, 117, 32, 115, 110, 32, 102, 32, 46, 115, 109, 32, 112, 109, 101, 99, 109, 102, 101, 97, 115, 32]', 8: '[104, 121, 32, 111, 110, 32, 115, 116, 110, 117, 32, 97, 102, 32, 32, 104, 105, 116, 32, 101, 97, 32, 114, 115, 32, 111, 101, 102, 116, 110, 116, 110]', 9: '', 10: '[32, 32, 111, 119, 32, 111, 32, 116, 32, 103, 114, 101, 114, 104, 101, 97, 117, 101, 111, 106, 101, 101, 102, 32, 104, 110, 116, 99, 97, 107, 100, 99]', 11: '[100, 116, 111, 105, 116, 32, 109, 111, 105, 101, 101, 44, 32, 101, 111, 114, 114, 32, 32, 117, 115, 99, 111, 84, 111, 116, 105, 117, 108, 101, 121, 101]', 12: '[101, 104, 112, 110, 104, 119, 111, 32, 116, 32, 32, 32, 116, 32, 112, 32, 101, 119, 109, 115, 32, 111, 117, 104, 117, 114, 109, 108, 111, 101, 105, 115]', 13: '[118, 101, 101, 32, 101, 105, 114, 108, 32, 116, 102, 119, 104, 100, 108, 100, 32, 111, 111, 116, 116, 110, 110, 101, 115, 121, 101, 116, 110, 112, 110, 115]', 14: '[101, 32, 114, 116, 32, 110, 101, 101, 105, 111, 111, 104, 101, 105, 101, 105, 111, 114, 115, 32, 104, 100, 100, 32, 97, 32, 44, 121, 101, 32, 103, 97]', 15: '[108, 119, 97, 104, 108, 32, 32, 97, 115, 32, 117, 105, 109, 102, 32, 102, 117, 100, 116, 105, 101, 108, 44, 104, 110, 102, 32, 32, 32, 116, 32, 114]', 16: '[111, 111, 116, 101, 111, 109, 97, 114, 32, 109, 114, 99, 46, 102, 102, 102, 116, 115, 32, 103, 109, 121, 32, 105, 100, 117, 116, 102, 116, 114, 116, 121]', 17: '[112, 114, 105, 32, 99, 111, 110, 110, 116, 97, 32, 104, 32, 101, 101, 101, 32, 32, 111, 110, 32, 44, 101, 115, 32, 108, 104, 111, 111, 97, 104, 32]', 18: '[109, 108, 111, 98, 97, 114, 100, 32, 104, 115, 116, 32, 65, 114, 101, 114, 116, 115, 102, 111, 104, 32, 115, 116, 121, 108, 101, 114, 32, 99, 101, 112]', 19: '[101, 100, 110, 111, 108, 101, 32, 109, 101, 116, 111, 105, 115, 101, 108, 101, 104, 111, 32, 114, 97, 67, 112, 111, 101, 32, 32, 32, 116, 101, 32, 97]', 20: '[110, 32, 32, 111, 32, 32, 109, 97, 32, 101, 110, 115, 32, 110, 32, 110, 101, 117, 116, 101, 118, 104, 101, 114, 97, 111, 111, 116, 104, 32, 112, 114]', 21: '[116, 105, 119, 109, 108, 67, 111, 110, 109, 114, 101, 32, 100, 116, 99, 116, 32, 110, 104, 32, 101, 105, 99, 121, 114, 102, 108, 104, 101, 111, 111, 116]', 22: '[32, 115, 105, 105, 97, 104, 114, 100, 111, 46, 115, 104, 105, 32, 111, 32, 109, 100, 101, 116, 32, 110, 105, 32, 115, 32, 100, 101, 32, 102, 101, 32]', 23: '[111, 32, 116, 110, 110, 105, 101, 97, 115, 10, 32, 97, 102, 109, 110, 116, 101, 32, 109, 104, 115, 101, 97, 111, 32, 99, 32, 32, 102, 32, 109, 108]', 24: '[102, 115, 104, 103, 103, 110, 32, 114, 116, 32, 105, 114, 102, 101, 102, 111, 97, 97, 32, 101, 112, 115, 108, 102, 109, 104, 112, 108, 111, 116, 115, 101]', 25: '[32, 101, 32, 32, 117, 101, 102, 105, 32, 32, 110, 100, 101, 97, 117, 110, 110, 108, 115, 32, 101, 101, 108, 32, 97, 97, 111, 111, 114, 104, 46, 97]', 26: '[67, 101, 67, 109, 97, 115, 111, 110, 100, 70, 32, 32, 114, 110, 115, 101, 105, 109, 112, 116, 99, 32, 121, 109, 107, 114, 101, 99, 101, 101, 32, 114]', 27: '[104, 107, 104, 97, 103, 101, 114, 44, 105, 105, 67, 116, 101, 105, 101, 115, 110, 111, 101, 111, 105, 108, 32, 111, 101, 109, 109, 97, 105, 32, 83, 110]', 28: '[105, 105, 105, 114, 101, 32, 101, 32, 102, 114, 104, 111, 110, 110, 100, 44, 103, 115, 97, 110, 97, 97, 116, 114, 115, 46, 32, 108, 103, 104, 111, 105]', 29: '[110, 110, 110, 107, 32, 99, 105, 98, 102, 115, 105, 32, 116, 103, 32, 32, 115, 116, 107, 101, 108, 110, 104, 101, 32, 32, 105, 32, 110, 105, 32, 110]', 30: '[101, 103, 97, 101, 104, 117, 103, 117, 105, 116, 110, 112, 32, 115, 119, 116, 44, 32, 105, 115, 32, 103, 101, 32, 116, 65, 115, 112, 101, 115, 105, 103]', 31: '[115, 32, 44, 116, 101, 115, 110, 116, 99, 108, 101, 114, 116, 44, 104, 104, 32, 116, 110, 44, 97, 117, 32, 116, 104, 116, 32, 101, 114, 116, 116, 32]'}
# DU_Encode(pkts, datas, 32)
