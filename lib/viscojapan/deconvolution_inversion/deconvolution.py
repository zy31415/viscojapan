from numpy import loadtxt

from ..least_square import LeastSquareTik2
from ..epochal_data import EpochalG, conv_stack, vstack_column_vec, \
     EpochalDisplacement
from ..inv_res_writer import WriterDeconvolution

class Deconvolution(LeastSquareTik2):
    def __init__(self):
        super().__init__()
        self.file_G = None
        self.file_d = None
        self.sites_filter_file = None

        self.nrows_slip = 10
        self.ncols_slip = 25

        self.row_norm_length = 1.
        self.col_norm_length = 28./23.03

        self.epochs = None
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

    def load_data(self):
        self.G = self._get_G()
        self.d = self._get_d()

    def get_filtered_sites(self):
        sites = loadtxt(self.sites_filter_file,'4a')
        return sites
        


