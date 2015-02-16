import numpy as np

from .epoch_sites_3d_array import EpochSites3DArray

__all__ = ['Displacement']

class Displacement(EpochSites3DArray):
    def __init__(self,
                 cumu_disp_3d,
                 epochs,
                 sites,
                 mask_sites=None):

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
        return self.get_cumu_at_nth_epoch(0)

    def get_coseismic_disp_hor_mag(self):
        tp = self.get_coseismic_disp()
        return np.sqrt(tp[:,0]**2 + tp[:,1]**2)

    def get_cumu_at_epoch(self, epoch):
        return self.get_data_at_epoch(epoch)

    def get_cumu_at_nth_epoch(self, nth):
        return self.get_data_at_nth_epoch(nth)

    def get_post_at_epoch(self, epoch):
        return self.get_data_at_epoch(epoch) - self.get_data_at_epoch(0)

    def get_post_at_nth_epoch(self, nth):
        return self.get_post_disp_3d()[nth,:,:]

    def get_post_hor_mag_at_epoch(self, epoch):
        tp = self.get_post_at_epoch(epoch)
        hor_mag = np.sqrt(tp[:,0]**2 + tp[:,1]**2)
        return hor_mag

    def get_post_hor_mag_at_nth_epoch(self, nth):
        tp = self.get_post_at_nth_epoch(nth)
        hor_mag = np.sqrt(tp[:,0]**2 + tp[:,1]**2)
        return hor_mag

    def get_velocity_hor_mag_at_epoch(self, epoch):
        tp = self.get_velocity_at_epoch(epoch)
        hor_mag = np.sqrt(tp[:,0]**2 + tp[:,1]**2)
        return hor_mag

    def cumu_ts(self,site, cmpt):
        return self._extract_time_series(self.get_cumu_disp_3d(), site, cmpt)

    def post_ts(self,site, cmpt):
        return self._extract_time_series(self.get_post_disp_3d(), site, cmpt)

    def vel_ts(self,site, cmpt):
        return self._extract_time_series(self.get_velocity_3d(), site, cmpt)

    def _extract_time_series(self, arr3d, site, cmpt):
        site_idx = self.get_index_in_mask_sites(site)
        cmpt_idx = 'enu'.index(cmpt)
        return arr3d[:,site_idx, cmpt_idx]

    @classmethod
    def load(cls,fid,
             mask_sites = None,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        if memory_mode:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        else:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY]

        epochs = fid['epochs'][...]
        sites = [site.decode() for site in fid['sites'][...]]

        return cls(cumu_disp_3d = array_3d,
                   epochs = epochs,
                   sites = sites,
                   mask_sites=mask_sites)




