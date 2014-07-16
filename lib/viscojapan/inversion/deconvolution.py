from numpy import loadtxt

from ..least_square import LeastSquareWithRegularization
from ..epochal_data import EpochalG, EpochalDisplacement, EpochalDisplacementSD
from .inversion import Inversion

class Deconvolution(Inversion):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 file_sites_filter,
                 epochs,
                 regularization,
                 basis,
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd
        self.file_sites_filter = file_sites_filter
        self.epochs = epochs

        super().__init__(
            regularization,
            basis_matrix,)

    def set_data_sd(self):
        sig = EpochalDisplacementSD(self.file_sd, self.file_sites_filter)
        sig_stacked = sig.vstack(self.epochs)
        _assert_column_vector(self.sd)

    def set_data_G(self):
        G_ep = EpochalG(self.file_G, self.file_sites_filter)
        G_stacked = G.conv_stack(self.epochs)

    def set_data_d(self):
        d_ep = EpochalDisplacement(self.file_d, self.file_sites_filter)
        self.d = disp.vstack(self.epochs)
        _assert_column_vector(self.d)
        
