# coding=utf-8

import random
import NetworkEnvironment as ne


class CoalitionGame:
    def __init__(self, coalitions, fds):
        self.coalitions = coalitions
        self.fds = fds

    '''
    联盟形成博弈过程，只博弈一轮，最后输出
    从一个联盟内随机取出一个
    '''
    def start(self, round, max_round):
        for c_a in self.coalitions:
            c_b = c_a
            while c_a == c_b:
                c_b = self.coalitions[random.randint(0, len(self.coalitions)-1)]

            a_fds, b_fds = c_a.could_swap_fds(c_b)
            if len(a_fds) >= 1 and len(b_fds) >= 1:
                fd_a = a_fds[random.randint(0, len(a_fds) - 1)]
                fd_b = b_fds[random.randint(0, len(b_fds) - 1)]
                if len(c_a.paired_fds) > len(c_b.paired_fds) + 2:
                    c_a.disconnect(fd_a)
                    fd_a.join_coalition(c_b)
                    print 'fd %d joined coalition %d' % (fd_a.num, c_b.num)
                elif len(c_a.paired_fds) + 2 < len(c_b.paired_fds):
                    c_b.disconnect(fd_b)
                    fd_b.join_coalition(c_a)
                    print 'fd %d joined coalition %d' % (fd_b.num, c_a.num)
                elif ne.need_swap(fd_a, fd_b, round, max_round):
                    fd_a.swap(fd_b)
                    print 'fd %d in coalition %d swap fd %d in coalition %d' % (fd_a.num, c_a.num, fd_b.num, c_b.num)
                # c_a.select_fd()
                # c_b.select_fd()

    def init_coalitions(self):
        for fd in self.fds:
            if len(fd.nearby_rus) >= 1:
                i = random.randint(0, len(fd.nearby_rus)-1)
                fd.join_coalition(fd.nearby_rus[i])
                print 'fd %d joined coalition %d' % (fd.num, fd.nearby_rus[i].num)