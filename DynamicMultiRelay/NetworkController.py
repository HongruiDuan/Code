#coding=utf-8

from BaseStation import BS
from RegisterUser import RU
from FogDevice import FD
from Coalition import Coalition
import matplotlib.pyplot as plt
import datetime
import os

class NetworkController:
    def __init__(self, positions):
        self.bs, self.coalitions, self.fds = self.create_net(positions)
        path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today())
        if os.path.exists(path) == True:
            times = 1
            while os.path.exists(path) == True:
                path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today()) + ' (' + str(times) + ')'
                times += 1

        self.path = path
        os.mkdir(self.path)  # 只mk 一次在net中mk
        self.gains_his = [0]
        self.fairness_his = [0]

    def create_net(self, positions):
        bs = BS(positions["BS"])
        coalitions = self.set_coalitions(positions["RUs"], bs)
        fds = self.set_fds(positions["FDs"])

        return bs, coalitions, fds

    def set_coalitions(self, positions, bs):
        coalitions = []
        for i in range(len(positions)):
            ru = RU('RU%d' % (i + 1), positions[i])
            c = Coalition(bs, ru, i)

            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % (i + 1), positions[i])
            fds.append(fd)
        return fds

    def show_coalitions(self, round):
        # 输出打印coalition
        # for i in self.coalitions:
        #     print i.ru.ruId #,"need power:",(i.ru.N * LossRate_BS(i.bs, i.ru) * i.ru.L / 100) * 0.004
        #     print "   RelaySet:",
        #     for j in i.RelaySet:
        #         print j.fdId,
        #     print
        #     print "   EHSet:",
        #     for j in i.EHSet:
        #         print j.fdId,
        #     print
        #     for j in i.fds:
        #         print "  ",j.fdId,"expect:",j.expect,"round:",j.round,"total:",j.total,"power:",j.power
        #    #print ""

        # 绘制图像保存
        # path = '../Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录

        plt.figure()

        plt.scatter(self.bs.position[0], self.bs.position[1], s=75, c='grey', marker='o')
        plt.annotate("BS", (self.bs.position[0], self.bs.position[1]))
        for i in self.fds:
            if i.coalition is None:
                plt.scatter(i.position[0], i.position[1], s=75, c='grey', marker='^')
                plt.annotate(i.fdId, (i.position[0], i.position[1]))

        colors = {
            'aliceblue': '#F0F8FF',
            'antiquewhite': '#FAEBD7',
            'aqua': '#00FFFF',
            'aquamarine': '#7FFFD4',
            'azure': '#F0FFFF',
            'beige': '#F5F5DC',
            'bisque': '#FFE4C4',
            'black': '#000000',
            'blanchedalmond': '#FFEBCD',
            'blue': '#0000FF',
            'blueviolet': '#8A2BE2',
            'brown': '#A52A2A',
            'burlywood': '#DEB887',
            'cadetblue': '#5F9EA0',
            'chartreuse': '#7FFF00',
            'chocolate': '#D2691E',
            'coral': '#FF7F50',
            'cornflowerblue': '#6495ED',
            'cornsilk': '#FFF8DC',
            'crimson': '#DC143C',
            'cyan': '#00FFFF',
            'darkblue': '#00008B',
            'darkcyan': '#008B8B',
            'darkgoldenrod': '#B8860B',
            'darkgray': '#A9A9A9',
            'darkgreen': '#006400',
            'darkkhaki': '#BDB76B',
            'darkmagenta': '#8B008B',
            'darkolivegreen': '#556B2F',
            'darkorange': '#FF8C00',
            'darkorchid': '#9932CC',
            'darkred': '#8B0000',
            'darksalmon': '#E9967A',
            'darkseagreen': '#8FBC8F',
            'darkslateblue': '#483D8B',
            'darkslategray': '#2F4F4F',
            'darkturquoise': '#00CED1',
            'darkviolet': '#9400D3',
            'deeppink': '#FF1493',
            'deepskyblue': '#00BFFF',
            'dimgray': '#696969',
            'dodgerblue': '#1E90FF',
            'firebrick': '#B22222',
            'floralwhite': '#FFFAF0',
            'forestgreen': '#228B22',
            'fuchsia': '#FF00FF',
            'gainsboro': '#DCDCDC',
            'ghostwhite': '#F8F8FF',
            'gold': '#FFD700',
            'goldenrod': '#DAA520',
            'gray': '#808080',
            'green': '#008000',
            'greenyellow': '#ADFF2F',
            'honeydew': '#F0FFF0',
            'hotpink': '#FF69B4',
            'indianred': '#CD5C5C',
            'indigo': '#4B0082',
            'ivory': '#FFFFF0',
            'khaki': '#F0E68C',
            'lavender': '#E6E6FA',
            'lavenderblush': '#FFF0F5',
            'lawngreen': '#7CFC00',
            'lemonchiffon': '#FFFACD',
            'lightblue': '#ADD8E6',
            'lightcoral': '#F08080',
            'lightcyan': '#E0FFFF',
            'lightgoldenrodyellow': '#FAFAD2',
            'lightgreen': '#90EE90',
            'lightgray': '#D3D3D3',
            'lightpink': '#FFB6C1',
            'lightsalmon': '#FFA07A',
            'lightseagreen': '#20B2AA',
            'lightskyblue': '#87CEFA',
            'lightslategray': '#778899',
            'lightsteelblue': '#B0C4DE',
            'lightyellow': '#FFFFE0',
            'lime': '#00FF00',
            'limegreen': '#32CD32',
            'linen': '#FAF0E6',
            'magenta': '#FF00FF',
            'maroon': '#800000',
            'mediumaquamarine': '#66CDAA',
            'mediumblue': '#0000CD',
            'mediumorchid': '#BA55D3',
            'mediumpurple': '#9370DB',
            'mediumseagreen': '#3CB371',
            'mediumslateblue': '#7B68EE',
            'mediumspringgreen': '#00FA9A',
            'mediumturquoise': '#48D1CC',
            'mediumvioletred': '#C71585',
            'midnightblue': '#191970',
            'mintcream': '#F5FFFA',
            'mistyrose': '#FFE4E1',
            'moccasin': '#FFE4B5',
            'navajowhite': '#FFDEAD',
            'navy': '#000080',
            'oldlace': '#FDF5E6',
            'olive': '#808000',
            'olivedrab': '#6B8E23',
            'orange': '#FFA500',
            'orangered': '#FF4500',
            'orchid': '#DA70D6',
            'palegoldenrod': '#EEE8AA',
            'palegreen': '#98FB98',
            'paleturquoise': '#AFEEEE',
            'palevioletred': '#DB7093',
            'papayawhip': '#FFEFD5',
            'peachpuff': '#FFDAB9',
            'peru': '#CD853F',
            'pink': '#FFC0CB',
            'plum': '#DDA0DD',
            'powderblue': '#B0E0E6',
            'purple': '#800080',
            'red': '#FF0000',
            'rosybrown': '#BC8F8F',
            'royalblue': '#4169E1',
            'saddlebrown': '#8B4513',
            'salmon': '#FA8072',
            'sandybrown': '#FAA460',
            'seagreen': '#2E8B57',
            'seashell': '#FFF5EE',
            'sienna': '#A0522D',
            'silver': '#C0C0C0',
            'skyblue': '#87CEEB',
            'slateblue': '#6A5ACD',
            'slategray': '#708090',
            'snow': '#FFFAFA',
            'springgreen': '#00FF7F',
            'steelblue': '#4682B4',
            'tan': '#D2B48C',
            'teal': '#008080',
            'thistle': '#D8BFD8',
            'tomato': '#FF6347',
            'turquoise': '#40E0D0',
            'violet': '#EE82EE',
            'wheat': '#F5DEB3',
            'white': '#FFFFFF',
            'whitesmoke': '#F5F5F5',
            'yellow': '#FFFF00',
            'yellowgreen': '#9ACD32'
        }
        colors = list(colors.keys())
        cindex = 0
        # 按照联盟来打点的颜色
        for i in self.coalitions:

            plt.scatter(i.ru.position[0], i.ru.position[1], s = 75, c=colors[cindex])
            plt.annotate(i.ru.ruId, (i.ru.position[0], i.ru.position[1]))

            for j in i.RelaySet:
                plt.scatter(j.position[0], j.position[1], s = 75, c=colors[cindex], marker='*')
                plt.annotate(j.fdId, (j.position[0], j.position[1]))

            for j in i.EHSet:
                plt.scatter(j.position[0], j.position[1], s = 75, c=colors[cindex], marker='^')
                plt.annotate(j.fdId, (j.position[0], j.position[1]))

            cindex += 1
        plt.savefig("%s/round%s.png" % (self.path, round))  # 保存图片
        plt.close()

    def gains_per_round(self, round):
        total = 0.0
        for i in self.fds:
            total += i.cumulative_utility
        self.gains_his.append(total)

    # 第一个版本的这种计算方法有点问题,fairness随着fd expect 变化
    def fairness_per_round(self, round):
        X = []
        for i in self.fds:
            if i.expect * round <= i.cumulative_utility:
                X.append(1.0)
            else:
                # 直到当前轮次之后的累积效用 / fd加入到联盟的期望效用 * 当前轮次
                X.append(i.cumulative_utility / i.expect * round)
        sum_of_xi = 0
        for i in range(0, len(X)):
            sum_of_xi += X[i]

        sum_of_xi2 = 0
        for i in range(0, len(X)):
            sum_of_xi2 += X[i] ** 2

        fairness = (sum_of_xi) ** 2 / (len(X) * sum_of_xi2)

        self.fairness_his.append(fairness)

    def save_result(self,maxround):
        # path = 'Pics/DynamicMultiRelay/' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录

        for i in self.fds:
            if i.coalition is not None:
                fig = plt.figure()

                plt.subplot(211)
                plt.xlabel('slot')
                plt.ylabel('Power(J) of %s' % i.fdId)
                data_x = [j for j in range(0, maxround+1)]
                data_pow = i.power_his
                labelx = range(1, maxround+2)
                plt.xticks(data_x, labelx, fontsize=14)
                plt.plot(data_x, data_pow, marker='*', label='%s pow' % i.fdId)
                plt.legend()  # 给图像加上图例

                plt.subplot(212)
                plt.xlabel('slot')
                plt.ylabel('Utility of %s' % i.fdId)
                data_x = [j for j in range(0, maxround+1)]
                data_utility = i.utility_his
                labelx = range(1, maxround+2)
                plt.xticks(data_x, labelx, fontsize=14)
                plt.plot(data_x, data_utility, marker='^',  label='%s utility' % i.fdId)

                plt.legend()  # 给图像加上图例
                plt.tight_layout()  # 解决重叠问题
                fig.savefig("%s/%s.png" % (self.path, i.fdId))  # 保存图片
                plt.close()

        # 绘制总的效用变化 和 fairness变化曲线
        plt.figure()
        plt.xlabel('slot')
        plt.ylabel('Total Throughput of all FDs')
        data_x = [j for j in range(0, maxround+1)]
        data_y1 = self.gains_his
        labelx = range(0, maxround+1)
        plt.xticks(data_x, labelx, fontsize=14)
        plt.plot(data_x, data_y1, marker='^',  label='Throughput')
        plt.legend()  # 给图像加上图例
        plt.savefig("%s/Throughput per slot.png" % (self.path))  # 保存图片
        plt.close()

        plt.figure()
        plt.xlabel('slot')
        plt.ylabel('Fairness of system')
        data_y2 = self.fairness_his
        data_x = [j for j in range(0, maxround + 1)]
        labelx = range(0, maxround + 1)
        plt.xticks(data_x, labelx, fontsize=14)
        plt.ylim(0,1)
        plt.plot(data_x, data_y2, marker='^', label='Fairness')
        plt.legend()  # 给图像加上图例
        plt.savefig("%s/Fairness per slot.png" % (self.path))  # 保存图片
        plt.close()

    # def show_powerhis(self, round):
    #     #path = 'Pics/DynamicMultiRelay' + str(datetime.date.today())  # 在net.py中调用是相对于net.py的目录
    #     for i in self.fds:
    #
    #
    # def show_utilityhis(self, round):

