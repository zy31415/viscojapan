import numpy as np

from .epoch_3d_array import Epoch3DArray

__all__ = ['Displacement']

class Displacement(Epoch3DArray):
    def __init__(self,
                 cumu_disp_3d,
                 epochs,
                 sites):
        assert epochs[0] == 0, 'The class is designed to represent slip that starts at t=0.'

        super().__init__(self, array3d=cumu_disp_3d, epochs=epochs)

        disp_shape = cumu_disp_3d.shape
        assert disp_shape[2] == 3, 'Displacement array should have three components.'

        self.sites = sites
        self.num_sites = len(self.sites)
        assert self.num_sites == disp_shape[1]

    # displacement as 3d
    @property
    def cumu_disp_3d(self):
        return self.array_3d

    @property
    def post_disp_3d(self):
        disp = self.cumu_disp_3d
        return disp - disp[0,:,:]

    def get_coseismic_disp(self):
        return self.cumu_disp_3d[0,:,:]

    def get_cumu_at_nth_epoch(self, nth):
        return self.get_data_at_nth_epoch(nth)

    def get_post_at_nth_epoch(self, nth):
        return self.post_disp_3d[nth,:,:]

    def cumu_ts(self,site, cmpt):
        return self._extract_time_series(self.cumu_disp_3d, site, cmpt)

    def post_ts(self,site, cmpt):
        return self._extract_time_series(self.post_disp_3d, site, cmpt)

    def vel_ts(self,site, cmpt):
        return self._extract_time_series(self.velocity_3d, site, cmpt)

    def _extract_time_series(self, arr3d, site, cmpt):
        site_idx = self.sites.index(site)
        cmpt_idx = 'enu'.index(cmpt)
        return arr3d[:,site_idx, cmpt_idx]



