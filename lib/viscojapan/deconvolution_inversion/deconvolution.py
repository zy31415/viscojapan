from ..least_square import LeastSquareTik2
from ..epochal_data import EpochalG, conv_stack, vstack_column_vec, EpochalDisplacement

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

    def get_G(self):
        G = EpochalG(self.file_G, self.sites_filter_file)
        G_stacked = conv_stack(G, self.epochs)
        return G_stacked
        
    def get_d(self):
        disp = EpochalDisplacement(self.file_d, self.sites_filter_file)
        d = vstack_column_vec(disp, self.epochs)
        return d
        

    
