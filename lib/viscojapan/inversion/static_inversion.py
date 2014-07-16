from viscojapan.epochal_data import EpochalG, EpochalDisplacement, EpochalDisplacementSD
from .inversion import Inversion
from ..utils import _assert_column_vector

class StaticInversion(Inversion):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 file_sites_filter,
                 regularization,
                 basis,                 
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd
        self.file_sites_filter = file_sites_filter
        
        super().__init__(
            regularization = regularization,
            basis = basis,)

    def set_data_sd(self):
        sig_ep = EpochalDisplacementSD(self.file_sd, self.file_sites_filter)
        self.sd = sig_ep(0)
        _assert_column_vector(self.sd)

    def set_data_G(self):
        G_ep = EpochalG(self.file_G, self.file_sites_filter)
        self.G = G_ep(0)

    def set_data_d(self):
        d_ep = EpochalDisplacement(self.file_d, self.file_sites_filter)
        self.d = d_ep(0)
        

