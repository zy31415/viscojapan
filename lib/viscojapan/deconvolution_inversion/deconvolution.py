import h5py

from numpy import loadtxt

from ..least_square import LeastSquareTik2
from ..epochal_data import EpochalG, conv_stack, vstack_column_vec, \
     EpochalDisplacement, break_col_vec_into_epoch_file
from ..utils import overrides
from ..inv_res_writer import WriterDeconvolution

class Deconvolution(LeastSquareTik2):
    def __init__(self):
        super().__init__()

        self.file_G = None
        self.file_d = None
        self.sites_filter_file = None
        self.epochs = None

        self.res_writer = WriterDeconvolution(self)

    def init(self):
        self.num_epochs = len(self.epochs)
        self.num_nlin_pars = 0

    @overrides(LeastSquareTik2)
    def _load_G(self):
        G = EpochalG(self.file_G, self.sites_filter_file)
        G_stacked = conv_stack(G, self.epochs)
        return G_stacked

    @overrides(LeastSquareTik2)
    def _load_d(self):
        disp = EpochalDisplacement(self.file_d, self.sites_filter_file)
        d = vstack_column_vec(disp, self.epochs)
        return d

    def get_filtered_sites(self):
        sites = loadtxt(self.sites_filter_file,'4a')
        return sites
        

    
