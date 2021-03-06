# -*- coding:utf-8 -*-
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from EH.newenergy import energy
from Params.params import getDistance
import numpy as np
np.set_printoptions(suppress=True)
import thread
import threading
import time
import json
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 16}) # 改变所有字体大小，改变其他性质类似
from NewGame import game
from fairness import Fairness

"线程函数"
def command(host, arg):
    result = host.cmd(arg)
    return result

class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
#设备类，存储设备的信息
'''
第一轮时初始化，在结束时将信息写入自己的缓存文件
如何更新信息

'''
random.seed(1)
class UE:
    count = 0
    def __init__(self, host, name, ip, port, link_e, num, gains=0.0, F_BS=0.0, F_UE=0.0, N1=0.0, b=0.0, Power = 0, flag=False):
        self.host = host
        self.name = name
        self.ip = ip
        self.port = port
        self.link_e = link_e
        self.num = num
        self.Power = random.uniform(0.001, 0.0015)
        self.gains = 0
        self.rank = 0
        self.powhis = [self.Power]
        UE.count += 1
def topology():
    #创建网络和设备初始化
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)
    #设备初始化
    ap1 = net.addAccessPoint('ap1', ssid="ap1-ssid", mode="g",
                             channel="1", position='5,6,0',range=40)
    AP = net.addStation('AP', position='5,10,0', ip='10.1.0.1', mac='00:00:00:00:00:EE') 

    UES = []
    for i in range(1,21):
        #创建中继设备节点
        temphost = net.addStation('DU%d'%i, position='%d,5,0'%(i+37), ip='10.0.0.%d'%i, mac='00:00:00:00:00:%02d'%i)
        #创建中继设备类对象
        temp = UE(temphost,'UE%d'%i,'10.0.0.%d'%i, 'DU%d-wlan0' %i,0.05+0.03*i,i) #丢包率已经初始化完毕
        UES.append(temp)
    
    #打印出设备池中的设备信息
    # for i in range(0,20):
    #     print(UES[i].name,UES[i].ip,UES[i].port,UES[i].Power,'\n')
    

    c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(AP, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    for i in range(0,len(UES)):
        net.addLink(UES[i].host, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    #设备初始化完毕，开始进行调度
    "总共进行10轮数据传输"
    Total_r = 20
    round = 0
    fair_result = []
    NFD = []
    FBS=[]
    FFD = []
    while round<Total_r:

        # info("***%d round AP collect info of UEs\n"% round)
        # try:
        #     thread.start_new_thread(command,(AP,"python RInfo.py 10.1.0.1 AP-wlan0"))
        #     print("python SInfo.py %s %s 10.1.0.1" % (UES[0].ip, UES[0].port))
        #     # print("python RInfo.py 10.1.0.1 AP-wlan0\n")
        #     thread.start_new_thread(command,(AP,"python RInfo.py 10.1.0.1 AP-wlan0"))
        #     for i in range(0,9):
        #         # print("python SInfo.py %s %s 10.1.0.1"%(UES[i].ip,UES[i].port))
        #         threading._start_new_thread(command,(UES[i].host,"python SInfo.py %s %s 10.1.0.1"%(UES[i].ip,UES[i].port)))   
        # except:
        #     print("%d round error\n" %round)
        # time.sleep(2.0 * UE.count) #根据中继设备的数量来确定等待时间
        # info("*** %d round info collect finish\n" % round)
        # 统计完设备信息之后将信息从文件中读取
        # 先采取直接对数据操作而不是真正的发送和接收包
        # filename1 = "/home/shlled/mininet-wifi/NCLog/BSLog.json"
        # with open(filename1,'r') as f1:
        #     buffer = f1.readlines()
        #     lenth = len(buffer)
        #     while lenth>0:
        #         temp = buffer[lenth-1]
        #         temp = json.loads(temp)
        #         # print(temp,"\n")
        #         #todo:如何确定所有的设备都已经接收完毕 

        #根据设备的丢包率来计算博弈结果，写入中继设备
        for i in range(0,20):
            result = game(1-UES[i].link_e)
            UES[i].F_BS = result[2]
            UES[i].F_UE = result[3]
            UES[i].N1 = result[0]
            UES[i].b = result[1]
        
        #根据设备能够达到的基站的效益对所有中继设备进行排序
        queue = sorted(UES, key = lambda UE: UE.F_BS, reverse=True)

        #打印中继设备的信息
        DeviceRank = []
        for i in range(0,20):
            DeviceRank.append(queue[i].num)
            print(queue[i].F_BS,queue[i].F_UE, queue[i].N1,queue[i].gains,queue[i].Power)
        print('%d-th round Device Rank:'%round, DeviceRank) 
        
        #开始发送信息
        num = 0
        while num<20:
            if (queue[num].N1*0.00004) < queue[num].Power:
                print('the %d-th device has been selected' % num)
                TotalTime = 10 #时间片大小
                # FileIndex = 0 #发送文件位置
                dst = []
                for i in range(0,20):
                    dst.append(queue[i].ip)
                #随机一个中继设备为RU
                dev_num = random.randint(0,20)
                #先不采用广播的方法
                for i in range(0,TotalTime):  #有100个最小时隙，AP广播100轮，DU选择接收能量和信息，RU直接接收信息  
                    "此处AP应该改成广播，APsend 的 dst应该不止一个"  
                    
                    # t1 = threading.Thread(target=command, args = (AP,"python APBroadCast.py 10.1.0.1 AP-wlan0 '%s' %s" %(dst,FileIndex)))#AP广播一个数据包
                    
                    #一个随机设备请求信息，因此其只接收信息
                    
                    # t2 = threading.Thread(target=command, args = (queue[dev_num].host,"python Receive.py %s %s 0.5"%(queue[dev_num].ip,queue[dev_num].port)))
                    
                    #其他的中继设备按照自身的丢包率来进行能量和信息收集
                    "先采用的是直接数值模拟，并没有进行实际的发送和接收包"
                    for j in range(0,len(UES)):
                        if (j+1) == queue[num].num:
                            top1 = int(100-100*UES[j].link_e)
                            key1 = random.randint(1,100)
                            "中继设备随机接收信息或者能量"
                            if key1 in range(1,top1):
                                pass
                            else:
                                
                                egy = energy(UES[j].host, AP, 0.011/TotalTime)
                                UES[j].Power += egy #第j个设备收集能量
                            # UES[j].powhis.append(egy)
                        else:
                            egy = energy(UES[j].host, AP, 0.011/TotalTime)
                            UES[j].Power += egy #第j个设备收集能量
                    # for i in range(0,20):
                    #     print(queue[i].Power,'\n')   
                    #先开始监听进程再开始发送进程
                    # t2.start()
                    # t1.start()
                    # t1.join()
                    # t2.join()
                    # t3.join()
                #被选中的中继设备将传输满足博弈均衡的有效信息量给请求的客户端设备
                #中继设备的发射功率为4mw，一个数据包为1k，中继设备的发射速率为100k/s
                "选中的中继设备通过中继减少能量，增加收益"
                #记录选中的设备
                NFD.append(queue[num].num)
                FBS.append(queue[num].F_BS)
                FFD.append(queue[num].F_UE)

                queue[num].Power -= queue[num].N1*0.00004
                queue[num].gains += queue[num].F_UE
                print("在第%d轮中，各中继设备的状态信息" % round)
                for k in range(0,20):
                    UES[k].powhis.append(UES[k].Power)#不管是否发送都要增加记录
                    print(UES[k].F_BS,UES[k].F_UE,UES[k].N1,'gain',UES[k].gains,'power',UES[k].Power)
                break


                #不采用多轮时隙的方法
                # for j in range(0,20):
                #     if j != dev_num:
                #         top1 = int(100-100*queue[j].link_e)
                #         key1 = random.randint(1,100)
                #         "中继设备随机接收信息或者能量,在基站广播的时候" 
                #         if key1 in range(1,top1):
                #             pass
                #             # info("DU%d infomation\n"% j)
                #             # t3 = threading.Thread(target = command,args = (UES[i].host,"python Receive.py %s %s 0.1"%(UES[j].ip,UES[j].port)))
                #         else:
                #             # info("DU%d energy\n"% j)
                #             egy = energy(UES[j].host, AP, 0.011)
                #             UES[j].Power += egy 
                #             # t3 = threading.Thread(target = energy,args = (UES[j].host,AP,1))                            
                #     #被选中的中继设备将传输满足博弈均衡的有效信息量给请求的客户端设备
                #     #中继设备的发射功率为4mw，一个数据包为1k，中继设备的发射速率为100k/s
                #     "选中的中继设备通过中继减少能量，增加收益"

                #     queue[num].Power -= queue[num].N1*0.00004
                #     queue[num].gains += queue[num].F_UE
                # print("在第%d轮中，各中继设备的状态信息" % round)
                # for i in range(0,20):
                #         print(UES[i].F_BS,UES[i].F_UE,UES[i].N1,'gain',UES[i].gains,'power',UES[i].Power)
                # break
            num += 1
        #如果所有中继设备能量都不够，则基站自己传输
        if num == 21:
            pass    
        #计算当前轮的fairness指数
        fair_result.append(Fairness(UES))
        round += 1
    plt.figure()
    plt.xlabel('round')
    plt.ylabel('Power(J)')
    # # 挑选比较有代表性的
    for i in range(0,len(UES)):
        if i in [0,1,2,3,11,19]:
            print("the power history of %d-th is"% UES[i].num, UES[i].powhis)
            data_x = [j for j in range(0,len(UES[i].powhis))]
            # round_x = range(len(UES[j].powhis))
            data_y = UES[i].powhis
            labelx = range(0,21)
            plt.xticks(data_x,labelx,fontsize = 14)
            plt.plot(data_x,data_y,marker = '*',label='%d-th'%UES[i].num)
    plt.legend()
    # plt.show()
    
    
    #绘制被选择的中继设备编号和基站和各中继设备的效益图
    plt.figure()
    round = [k for k in range(0,20)]
    plt.plot(round, FBS, marker='o', label="$U_{BS}$")
    plt.plot(round, FFD, marker='*', label="$U_{FD}$")
    # for i in range(0,len(UES)):
    #     plt.annotate(NFD[i], (round[i], FBS[i]))
    #     plt.annotate(NFD[i], (round[i], FFD[i]))
    labelx = range(1,21)
    plt.xticks(round,labelx,fontsize = 14)
    plt.xlabel('round')
    plt.ylabel("Utility of BS and FD")
    plt.ylim(80,280)
    plt.grid()
    plt.legend()
    plt.show()



    info("*** Fairness")
    print(fair_result)
    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

