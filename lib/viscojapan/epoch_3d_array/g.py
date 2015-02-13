import numpy as np

__author__ = 'zy'

from .epoch_sites_3d_array import EpochSites3DArray

class G(EpochSites3DArray):
    def __init__(self,
                 g_3d,
                 epochs,
                 sites,
                 mask_sites):

        assert epochs[0] == 0, 'The class is designed to represent slip that starts at t=0.'

        assert len(sites)*3 == g_3d.shape[1]

        super().__init__(array_3d=g_3d, epochs=epochs, sites=sites, mask_sites=mask_sites)

        self._num_subflts = g_3d.shape[2]


    def get_num_subflts(self):
        return self._num_subflts

    def get_mask(self):
        ch = super().get_mask()
        ch1 = np.asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1

