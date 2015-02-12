import numpy as np

from .epoch_file_reader import EpochFileReader
from ...utils import as_string

__all__ = ['EpochSitesFileReader']


class EpochSitesFileReader(EpochFileReader):
    def __init__(self,
                 file_name,
                 mask_sites=None):
        super().__init__(file_name)


        assert self.has_info('sites'), 'File %s should have sites information.'\
               %self.file_name
        self._sites = as_string(self['sites'][...])

        if mask_sites is None:
            mask_sites = self.sites
        else:
            # assert in all_sites list:
            for site in mask_sites:
                assert site in self.sites, 'Site %s is not in all sites list'%(site)

        self._mask_sites = mask_sites
        

    @property
    def mask_sites(self):
        return self._mask_sites

    @property
    def sites(self):
        return self._sites

    def _gen_mask(self):
        raise NotImplementedError()

    def get_data_at_epoch(self,time):
        out = super().get_data_at_epoch(time)
        ch = self._gen_mask()
        return out[ch,:]



