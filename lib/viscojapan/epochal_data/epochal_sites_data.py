from os.path import exists

import h5py
from numpy import loadtxt, asarray, zeros

from .epochal_data import EpochalData
from ..utils import overrides

class EpochalSitesData(EpochalData):
    ''' Wrapper of sites data. 
1. epoch_file must be present.
2. "sites" key word must be present in info dataset.
'''
    def __init__(self, epoch_file):
        assert exists(epoch_file), "File %s must be present."%epoch_file
        super().__init__(epoch_file)
        assert self.has_info('sites'), "'sites' key word must be present."

    @property
    def sites(self):
        return self.get_info('sites')

    @sites.setter
    def sites(self, sites):
        self.set_info('sites', sites)

    def get_site_cmpt_idx(self, site, cmpt):
        sites = self.sites
        idx1 = list(sites).index(site.encode())
        if cmpt == 'e':
            idx2 = 3*idx1
        elif cmpt == 'n':
            idx2 = 3*idx1 + 1
        elif cmpt == 'u':
            idx2 = 3*idx1 + 2
        else:
            raise ValueError('No such component.')
        return idx2

    def get_epoch_value_at_site(self, site, cmpt, epoch):
        idx = self.get_site_cmpt_idx(site, cmpt)
        res = self.get_epoch_value(epoch)
        return res[idx]

    def set_value_at_site(self, site, cmpt, epoch, value):
        idx = self.get_site_cmpt_idx(site, cmpt)
        self.set_value(epoch, idx, value)

class EpochalSitesFilteredData(EpochalSitesData):
    def __init__(self, epoch_file,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(epoch_file)
        if (filter_sites_file is None) and (filter_sites is None):
            self.filter_sites = self.sites
        elif (filter_sites_file is not None) and (filter_sites is not None):
            raise ValueError("Don't offer filter_sites and filter_sites_file at the same time.")
        elif filter_sites_file is not None:
            self.filter_sites_file = filter_sites_file
        elif filter_sites is not None:
            self.filter_sites = filter_sites

    @property
    def filter_sites_file(self):
        return self._filter_sites_file

    @filter_sites_file.setter
    def filter_sites_file(self, filter_sites_file):
        assert exists(filter_sites_file), \
               "File %s doesn't exist."%filter_sites_file
        self._filter_sites_file = filter_sites_file
        self.filter_sites = loadtxt(self.filter_sites_file,'4a,')    

    @property
    def filter_sites(self):
        return self._filter_sites

    @filter_sites.setter
    def filter_sites(self, filter_sites):
        self._assert_in_sites_list(filter_sites)
        self._filter_sites_file = None
        self._filter_sites = filter_sites

    def _assert_in_sites_list(self, sites):
        sites_original = self.sites
        for site in sites:
            assert site in sites_original,\
                   "%s is not included in sites list of epochal data."%site

    def _gen_filter(self):
        sites_original = list(self.get_info('sites'))
        ch = []
        for site in self.filter_sites:
            ch.append(sites_original.index(site))
        ch = asarray(ch)
        ch1 = asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

    @overrides(EpochalSitesData)
    def get_epoch_value(self,time):
        out = super().get_epoch_value(time)
        ch = self._gen_filter()
        return out[ch,:]

class EpochalG(EpochalSitesFilteredData):
    def __init__(self,epoch_file, filter_sites_file):
        super().__init__(epoch_file, filter_sites_file)

class EpochalDisplacement(EpochalSitesFilteredData):
    def __init__(self,epoch_file, filter_sites_file):
        super().__init__(epoch_file, filter_sites_file)

    def get_time_series(self, site, cmpt):
        epochs = self.get_epochs()
        ys = zeros(len(epochs))
        for nth, epoch in enumerate(epochs):
            ys[nth] = self.get_epoch_value_at_site(site, cmpt, epoch)
        return ys
    
class EpochalDisplacementSD(EpochalSitesFilteredData):
    def __init__(self,epoch_file, filter_sites_file):
        super().__init__(epoch_file, filter_sites_file)

    @overrides(EpochalSitesFilteredData)
    def get_epoch_value(self, epoch):
        out = self._get_epoch_value(epoch)
        ch = self._gen_filter()
        return out[ch,:]
        
    
