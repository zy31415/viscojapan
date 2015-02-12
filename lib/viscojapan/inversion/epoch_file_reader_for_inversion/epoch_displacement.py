import numpy as np

from .epochal_sites_file_reader import EpochalSitesFileReader

__author__ = 'zy'
__all__ = ['EpochalDisplacement', 'EpochalDisplacementSD']

class EpochalDisplacement(EpochalSitesFileReader):
    def __init__(self,file_name,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(file_name, filter_sites_file, filter_sites)

    def _gen_mask(self):
        ch = []
        for site in self.mask_sites:
            ch.append(self.sites.index(site))
        ch = np.asarray(ch)
        return ch

    def stack(self, epochs):
        return np.vstack([self.get_data_at_epoch(epoch).reshape([-1,1]) for epoch in epochs])


class EpochalDisplacementSD(EpochalDisplacement):
    def __init__(self,file_name,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(file_name, filter_sites)

    def get_data_at_epoch(self, epoch):
        assert epoch in self.epochs, "EpochalDisplacementSD doesn't allow interpolation."
        super().get_data_at_epoch()