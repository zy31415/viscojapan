import numpy as np
import h5py

import viscojapan as vj
from viscojapan.epochal_data import EpochalG, EpochalDisplacement, EpochalDisplacementSD
from .inversion import Inversion
from ..utils import assert_col_vec_and_get_nrow

class StaticInversion(Inversion):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 file_sites_filter,
                 regularization,
                 basis,
                 epoch = 0,
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd
        self.file_sites_filter = file_sites_filter
        self.epoch = epoch
        
        super().__init__(
            regularization = regularization,
            basis = basis,)

    def set_data_sd(self):
        sig_ep = EpochalDisplacementSD(self.file_sd, self.file_sites_filter)
        self.sd = sig_ep(self.epoch)
        assert_col_vec_and_get_nrow(self.sd)

    def set_data_G(self):
        G_ep = EpochalG(self.file_G, self.file_sites_filter)
        self.G = G_ep(0)

    def set_data_d(self):
        d_ep = EpochalDisplacement(self.file_d, self.file_sites_filter)
        self.d = d_ep(self.epoch)

    def save(self, fn, overwrite = False):
        super().save(fn, overwrite)
        sites = np.loadtxt(self.file_sites_filter,'4a')
        ch_inland = vj.choose_inland_GPS_for_cmpts(sites)
        with h5py.File(fn) as fid:
            fid['sites'] = sites
            fid['misfit/rms_inland'] = self.get_residual_rms(subset=ch_inland)
            
            
        

