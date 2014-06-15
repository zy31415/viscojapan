from os.path import exists

import h5py
from numpy import loadtxt, asarray

from .epochal_data import EpochalData

class EpochalSitesData(EpochalData):
    ''' Wrapper of sites data. 
1. epoch_file must be present.
2. "sites" key word must be present in info dataset.
'''
    def __init__(self, epoch_file):
        assert exists(epoch_file), "File %s must be present."%epoch_file
        super().__init__(epoch_file)
        assert self.has_info('sites'), "'sites' key word must be present."
        

class EpochalSitesFilteredData(EpochalSitesData):
    def __init__(self, epoch_file, filter_sites_file):
        super().__init__(epoch_file)

        assert exists(filter_sites_file), \
               "File %s doesn't exist."%filter_sites_file
        self.filter_sites_file = filter_sites_file
        filter_sites = loadtxt(self.filter_sites_file,'4a,')
        self._assert_in_site_list(filter_sites)
        self.filter_sites = filter_sites                                                 

    def _assert_in_site_list(self, sites):
        # assert sites are in original sites list
        sites_original = self.get_info('sites')
        for site in sites:
            assert site in sites_original, 'No data about %s.'%site

    def _gen_filter(self):
        sites_original = list(self.get_info('sites'))
        ch = []
        for site in self.filter_sites:
            ch.append(sites_original.index(site))
        ch = asarray(ch)
        ch1 = asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

    def get_epoch_value(self,time):
        out = super().get_epoch_value(time)
        ch = self._gen_filter()
        return out[ch,:]
