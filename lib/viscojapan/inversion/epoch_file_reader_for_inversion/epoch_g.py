import numpy as np

__author__ = 'zy'

class EpochG(EpochalSitesFilteredData):
    def __init__(self,epoch_file,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(epoch_file, filter_sites_file, filter_sites)

    def stack(self, epochs):
        N = len(epochs)

        sh1, sh2 = self.get_data_at_epoch(0).shape

        G = np.zeros((sh1*N, sh2*N), dtype='float')
        for nth in range(0, N):
            t1 = epochs[nth]
            for mth in range(nth, N):
                t2 = epochs[mth]
                #print(t2,t1,t2-t1)
                G_ = self.get_data_at_epoch(t2-t1)
                #print(mth*sh1,(mth+1)*sh1,nth*sh2,(nth+1)*sh2)
                G[mth*sh1:(mth+1)*sh1,
                  nth*sh2:(nth+1)*sh2] = G_
        return G