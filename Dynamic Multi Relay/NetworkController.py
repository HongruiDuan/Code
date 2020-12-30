#coding=utf-8

from BaseStation import BS
from RegisterUser import RU
from FogDevice import FD
from Coalition import Coalition
class NetworkController:
    def __init__(self,positions):
        self.bs, self.coalitions, self.fds = self.create_net(positions)


    def create_net(self, positions):

        bs = BS(positions["BS"])
        coalitions = self.set_coalitions(positions["RUs"], bs)
        fds = self.set_fds(positions["FDs"])

        return bs, coalitions, fds

    def set_coalitions(self, positions, bs):
        coalitions = []
        for i in range(len(positions)):
            ru = RU('RU%d' % i, positions[i])
            c = Coalition(bs, ru, i)
            c.bs = bs
            coalitions.append(c)
        return coalitions

    def set_fds(self, positions):
        fds = []
        for i in range(len(positions)):
            fd = FD('FD %d' % i, positions[i])
            fds.append(fd)
        return fds

    def show_coalitions(self):
        for i in self.coalitions:
            print i.ru.ruId,":",
            for j in i.fds:
                print j.fdId,
            print
            print "   RelaySet:",
            for j in i.RelaySet:
                print j.fdId,
            print
            print "   EHSet:",
            for j in i.EHSet:
                print j.fdId,
            print