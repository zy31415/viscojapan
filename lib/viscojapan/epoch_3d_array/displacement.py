import numpy as np

from .epoch_sites_3d_array import EpochSites3DArray

__all__ = ['Displacement']

class Displacement(EpochSites3DArray):
    def __init__(self,
                 cumu_disp_3d,
                 epochs,
                 sites,
                 mask_sites):

        assert epochs[0] == 0, 'The class is designed to represent slip that starts at t=0.'

        assert cumu_disp_3d.shape[1] == len(sites)
        assert cumu_disp_3d.shape[2] == 3, 'Displacement array should have three components.'

        super().__init__(array_3d=cumu_disp_3d, epochs=epochs, sites=sites, mask_sites=mask_sites)


    # displacement as 3d
    def get_cumu_disp_3d(self):
        return self.get_array_3d()

    def get_post_disp_3d(self):
        disp = self.get_cumu_disp_3d()
        return disp - disp[0,:,:]

    def get_coseismic_disp(self):
        return self.get_cumu_disp_3d[0,:,:]

    def get_cumu_at_nth_epoch(self, nth):
        return self.get_data_at_nth_epoch(nth)

    def get_post_at_nth_epoch(self, nth):
        return self.get_post_disp_3d[nth,:,:]

    def cumu_ts(self,site, cmpt):
        return self._extract_time_series(self.get_cumu_disp_3d, site, cmpt)

    def post_ts(self,site, cmpt):
        return self._extract_time_series(self.get_post_disp_3d, site, cmpt)

    def vel_ts(self,site, cmpt):
        return self._extract_time_series(self.get_velocity_3d, site, cmpt)

    def _extract_time_series(self, arr3d, site, cmpt):
        site_idx = self.sites.index(site)
        cmpt_idx = 'enu'.index(cmpt)
        return arr3d[:,site_idx, cmpt_idx]

    def get_mask(self):
        ch = []
        for site in self.mask_sites:
            ch.append(self.sites.index(site))
        ch = np.asarray(ch)
        ch1 = np.asarray([ch*3, ch*3+1, ch*3+2]).T.flatten()
        return ch1



