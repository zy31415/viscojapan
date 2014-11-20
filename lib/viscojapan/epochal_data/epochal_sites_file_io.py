import numpy as np

from .epochal_file_io import EpochalFileReader

from ..utils import overrides, as_string

__all__ = ['EpochalSitesFileReader']


class EpochalSitesFileReader(EpochalFileReader):
    def __init__(self, epoch_file,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(epoch_file)

        self._filter_sites_file = filter_sites_file
        self._filter_sites = filter_sites
        self._init_filter_sites_file_and_filter_sites()
        

    def _init_filter_sites_file_and_filter_sites(self):
        assert self.has_info('sites'), 'File %s should have sites information.'\
               %self.file_name

        self._all_sites = as_string(self['sites'])
        
        if (self._filter_sites_file is None) and (self._filter_sites is None):            
            self._filter_sites = self._all_sites
        elif (self._filter_sites_file is not None) and (self._filter_sites is not None):
            raise ValueError("Don't offer filter_sites and filter_sites_file at the same time.")
        elif self._filter_sites_file is not None:
            self._filter_sites = as_string(
                np.loadtxt(self._filter_sites_file, '4a', usecols=(0,)))
        elif self._filter_sites is not None:
            self._filter_sites_file = None

        # assert in all_sites list:
        for site in self._filter_sites:
            assert site in self._all_sites, 'Site %s is not in all sites list'%(site)
        
    @property
    def filter_sites_file(self):
        return self._filter_sites_file

    @property
    def filter_sites(self):
        return self._filter_sites

    @property
    def all_sites(self):
        return self._all_sites

    def _gen_filter(self):
        ch = []
        for site in self.filter_sites:
            ch.append(self.all_sites.index(site))
        ch = np.asarray(ch)
        ch1 = np.asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

    @overrides(EpochalFileReader)
    def get_epoch_value(self,time):
        out = super().get_epoch_value(time)
        ch = self._gen_filter()
        return out[ch,:]

