import h5py

from numpy import loadtxt

from ..least_square import LeastSquare, SpatialTemporalReg
from ..epochal_data import EpochalG, conv_stack, vstack_column_vec, \
     EpochalDisplacement
from ..utils import overrides
from ..inv_res_writer import WriterDeconvolution

class Deconvolution(LeastSquare):
    def __init__(self):
        super().__init__()

        self.file_G = None
        self.file_d = None
        self.sites_filter_file = None
        self.epochs = None

        self.nrows_slip = 10
        self.ncols_slip = 25
        self.row_norm_length = 1.
        self.col_norm_length = 28./23.03

        self.num_nlin_pars = 0

        self.res_writer = WriterDeconvolution(self)

    def _get_G(self):
        G = EpochalG(self.file_G, self.sites_filter_file)
        G_stacked = conv_stack(G, self.epochs)
        return G_stacked

    def _get_d(self):
        disp = EpochalDisplacement(self.file_d, self.sites_filter_file)
        d = vstack_column_vec(disp, self.epochs)
        return d

    def _get_reg_mat(self, alpha, beta):
        reg = SpatialTemporalReg()
        reg.nrows_slip = self.nrows_slip
        reg.ncols_slip = self.ncols_slip
        reg.row_norm_length = self.row_norm_length
        reg.col_norm_length = self.col_norm_length

        reg.epochs = self.epochs
        reg.num_nlin_pars = self.num_nlin_pars

        self.regularization_matrix = reg

        mat = reg(alpha=alpha, beta=beta)
        return mat

    def load_data(self):
        self.G = self._get_G()
        self.d = self._get_d()

    @overrides(LeastSquare)    
    def invert(self, alpha, beta):        
        self.L = self._get_reg_mat(alpha, beta)
        self.solution = super().invert()
        self.alpha = alpha
        self.beta = beta

    def get_filtered_sites(self):
        sites = loadtxt(self.sites_filter_file,'4a')
        return sites

    def get_spatial_roughness(self):
        return self.regularization_matrix.get_spatial_roughness(self.m)

    def get_temporal_roughness(self):
        return self.regularization_matrix.get_temporal_roughness(self.m)

    def num_epochs(self):
        return len(self.epochs)
        

    
