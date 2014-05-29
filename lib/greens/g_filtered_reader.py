from os.path import exists

import h5py
from numpy import loadtxt, asarray

from .g_reader import GReader

class GFilteredReader(GReader):
    ''' Fliter a G matrix according a new station list.
'''
    def __init__(self, fG, sites_file):
        super().__init__(fG)        
        self.sites_file = sites_file

        self._init()

    def _init(self):
        assert exists(self.sites_file), "File %s doesn't exist."%self.fG

        # assert sites are in original sites list
        sites = loadtxt(self.sites_file,'4a,')
        sites_original = self.get_info('sites')
        for site in sites:
            assert site in sites_original, 'No data about %s.'%site
        self.sites = sites

    def _gen_filter(self):
        sites_original = list(self.get_info('sites'))
        ch = []
        for site in self.sites:
            ch.append(sites_original.index(site))
        ch = asarray(ch)
        ch1 = asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

    def get_epoch_value(self,time):
        out = super().get_epoch_value(time)
        ch = self._gen_filter()
        return out[ch,:]
