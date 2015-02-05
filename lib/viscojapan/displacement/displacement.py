import numpy as np

from ..sites import Site

__all__ = ['Disp']

class Disp(object):
    def __init__(self,
                 cumu_disp3d,
                 epochs,
                 sites):
        self._cumu_disp3d = cumu_disp3d
        disp_shape = cumu_disp3d.shape
        assert len(disp_shape) == 3

        self.epochs = epochs
        self.num_epochs = len(self.epochs)
        assert disp_shape[0] == self.num_epochs

        self.sites = sites
        assert isinstance(self.sites, list)
        for site in sites:
            assert isinstance(site, Site)
        self.num_sites = len(self.sites)
        assert self.num_sites == disp_shape[1]

        # three components
        assert disp_shape[2] == 3

    @property
    def cumu3d(self):
        return self._cumu_disp3d

    @property
    def post3d(self):
        disp = self.cumu3d
        return disp - disp[0,:,:]

    @property
    def vel3d(self):
        dt = np.diff(self.epochs).reshape([-1,1,1])
        vel = np.diff(self.cumu3d, axis=0)/dt # meter/day
        return vel

    def get_vel3d(self, unit='mm/yr'):
        vel = self.vel3d
        if unit == 'm/d':
            return vel
        elif unit == 'mm/yr':
            return vel*1000*365
        else:
            raise ValueError('unit not defined.')

    def get_co_disp(self):
        assert self.epochs[0] == 0
        return self._cumu_disp3d[0]

    def get_cumu_at_nth_epoch(self, nth):
        return self.cumu3d[nth,:,:]

    def get_post_at_nth_epoch(self, nth):
        return self.post3d[nth,:,:]

    def cumu_ts(self,site, cmpt):
        return self._extract_time_series(self.cumu3d, site, cmpt)

    def post_ts(self,site, cmpt):
        return self._extract_time_series(self.post3d, site, cmpt)

    def vel_ts(self,site, cmpt):
        return self._extract_time_series(self.vel3d, site, cmpt)

    def _extract_time_series(self, arr3d, site, cmpt):
        site_idx = self.sites.index(site)
        cmpt_idx = 'enu'.index(cmpt)
        return arr3d[:,site_idx, cmpt_idx]



