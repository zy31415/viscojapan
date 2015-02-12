import numpy as np

from .epoch_sites_file_reader import EpochSitesFileReader

__author__ = 'zy'
__all__ = ['EpochDisplacement', 'EpochDisplacementSD']

class EpochDisplacement(EpochSitesFileReader):
    def __init__(self,file_name,
                 mask_sites=None):
        super().__init__(file_name, mask_sites)

    def _gen_mask(self):
        ch = []
        for site in self.mask_sites:
            ch.append(self.sites.index(site))
        ch = np.asarray(ch)
        return ch

    def stack(self, epochs):
        return np.vstack([self.get_data_at_epoch(epoch).reshape([-1,1]) for epoch in epochs])


class EpochDisplacementSD(EpochDisplacement):
    def __init__(self,file_name,
                 mask_sites=None):
        super().__init__(file_name, mask_sites)

    def get_data_at_epoch(self, epoch):
        assert epoch in self.epochs, "EpochalDisplacementSD doesn't allow interpolation."
        return super().get_data_at_epoch(epoch)