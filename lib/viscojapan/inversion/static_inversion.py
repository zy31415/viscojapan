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
                 filter_sites_file,
                 regularization,
                 basis,
                 epoch = 0,
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd
        
        self.filter_sites_file = filter_sites_file
        self.sites = np.loadtxt(self.filter_sites_file,'4a,', usecols=(0,))

        self.epoch = epoch
        self.epochs = [epoch]
        self.nlin_par_names = []

        
        
        super().__init__(
            regularization = regularization,
            basis = basis,)

    def set_data_sd(self):
        sig_ep = EpochalDisplacementSD(self.file_sd, self.filter_sites_file)
        self.sd = sig_ep[self.epoch]
        assert_col_vec_and_get_nrow(self.sd)

    def set_data_G(self):
        G_ep = EpochalG(self.file_G, self.filter_sites_file)
        self.G = G_ep[0]

    def set_data_d(self):
        d_ep = EpochalDisplacement(self.file_d, self.filter_sites_file)
        self.d = d_ep[self.epoch]

