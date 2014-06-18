import h5py

from numpy import loadtxt

from ..least_square import LeastSquareTik2
from ..epochal_data import EpochalG, conv_stack, vstack_column_vec, \
     EpochalDisplacement, break_col_vec_into_epoch_file
from ..utils import overrides

class Deconvolution(LeastSquareTik2):
    def __init__(self):
        super().__init__()

        self.file_G = None
        self.file_d = None
        self.sites_filter_file = None
        self.epochs = None

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
        
    @overrides(LeastSquareTik2)
    def save_results(self, fn):
        super().save_results(fn)
        with h5py.File(fn) as fid:
            fid['num_nlin_pars'] = self.num_nlin_pars
            fid['epochs'] = self.epochs
            fid['num_epochs'] = self.num_epochs
            fid['sites'] = self.get_filtered_sites()

    def save_results_slip(self, fn):
        break_col_vec_into_epoch_file(self.m, self.epochs, fn)

    def save_results_pred_disp(self, fn):
        info = {'sites':self.get_filtered_sites()}
        break_col_vec_into_epoch_file(self.d, self.epochs, fn,
                                      info_dic = info)
        
            
        
        
        

    
