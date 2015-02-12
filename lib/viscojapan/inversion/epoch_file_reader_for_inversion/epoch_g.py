import numpy as np

from .epochal_sites_file_reader import EpochalSitesFileReader

__author__ = 'zy'
__all__ = ['EpochG','DifferentialG']

def stack_G_for_convolution(self, epochs):
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


class EpochG(EpochalSitesFileReader):
    def __init__(self,file_name,
                 filter_sites=None):
        super().__init__(file_name, filter_sites)

    def _gen_mask(self):
        ch = []
        for site in self.mask_sites:
            ch.append(self.sites.index(site))
        ch = np.asarray(ch)
        ch1 = np.asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

    # Monkey Patch :-)
    stack = stack_G_for_convolution



class DifferentialG(object):
    ''' This class computes the diffretial of two EpochData objects
with respcet to (wrt) the change of an indicated variable.
'''
    def __init__(self, ed1, ed2, wrt):
        ''' Arguments:
ed1 : object of EpochalData
ed2 : object of EpochalData
wrt - with respect to, variable that the change WRT.
'''
        self.ed1 = ed1
        self.ed2 = ed2
        self.wrt = wrt

        self._init()

    def _init(self):
        assert self.ed1.has_info(self.wrt)
        assert self.ed2.has_info(self.wrt)

        self._get_vars()

    def _get_vars(self):
        self.var1 = float(self.ed1.get_info(self.wrt))
        setattr(self, self.wrt+'1', self.var1)

        self.var2 = float(self.ed2.get_info(self.wrt))
        setattr(self, self.wrt+'2', self.var2)

    def get_data_at_epoch(self, day):
        G1 = self.ed1.get_data_at_epoch(day)
        G2 = self.ed2.get_data_at_epoch(day)
        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.get_data_at_epoch(name)
        else:
            raise ValueError('Not recognized type.')

    # Monkey Patch :-)
    stack = stack_G_for_convolution