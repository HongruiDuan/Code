class BS:
    # todo: is value right
    def __init__(self,position,W=2500000000.0, N=1.0, P_T=60.0, G_T=0.0, G_R=0.0):
        #self.host = host

        self.position = position
        self.W = W
        self.N = N
        self.P_T = P_T
        self.G_T = G_T
        self.G_R = G_R

        # rf sender value
        self.rf_W = 900000000.0
        self.rf_p_t = 6000
        self.rf_g_t = 2
        self.rf_g_r = 2