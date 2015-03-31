import numpy as np
import h5py

import viscojapan as vj
from .epoch_file_reader_for_inversion import EpochDisplacementSD, EpochDisplacement, EpochG
from .inversion import Inversion
from ..utils import assert_col_vec_and_get_nrow, as_string

__all__ = ['StaticInversion', 'PostseismicStaticInversion']

class StaticInversion(Inversion):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 filter_sites_file,
                 regularization,
                 basis,
                 fault_file,
                 epoch = 0,
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd

        self.sites = as_string(np.loadtxt(filter_sites_file,'4a,', usecols=(0,)))

        self.epoch = epoch
        self.epochs = [epoch]
        self.num_epochs = len(self.epochs)
        self.nlin_par_names = []

        reader = vj.fm.FaultFileReader(fault_file)
        self.num_subflt_along_dip = reader.num_subflt_along_dip
        self.num_subflt_along_strike = reader.num_subflt_along_strike

        
        
        super().__init__(
            regularization = regularization,
            basis = basis,)

    def set_data_sd(self):
        sig_ep = EpochDisplacementSD(self.file_sd,
                                     mask_sites = self.sites)
        self.sd = sig_ep[self.epoch].reshape([-1,1])
        assert_col_vec_and_get_nrow(self.sd)

    def set_data_G(self):
        G_ep = EpochG(self.file_G,
                      mask_sites=self.sites
                      )
        self.G = G_ep[0]

    def set_data_d(self):
        d_ep = EpochDisplacement(
            self.file_d,
            mask_sites=self.sites
        )
        self.disp_obs = self.d = d_ep.get_cumu_at_epoch(self.epoch).reshape([-1,1])

class PostseismicStaticInversion(StaticInversion):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 filter_sites_file,
                 regularization,
                 basis,
                 fault_file,
                 epoch = 0,
                 ):
        super().__init__(
            file_G = file_G,
            file_d = file_d,
            file_sd = file_sd,
            filter_sites_file = filter_sites_file,
            regularization = regularization,
            basis = basis,
            fault_file = fault_file,
            epoch = epoch,
        )

    def set_data_d(self):
        d_ep = EpochDisplacement(
            self.file_d,
            mask_sites=self.sites
        )
        self.disp_obs = self.d = d_ep.get_post_at_epoch(self.epoch).reshape([-1,1])
