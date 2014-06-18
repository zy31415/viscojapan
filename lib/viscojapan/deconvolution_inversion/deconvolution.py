from ..least_square import LeastSquareTik2

class Deconvolution(LeastSquareTik2):
    def __init__(self):
        super().__init__()

        self.G_file = None
        self.d_file = None
        self.sites_filter_file = None
        self.epochs = None

    def init(self):
        self.num_epochs = len(self.epochs)
        self.num_nlin_pars = 0

    def get_G(self):
        G = EpochalG(self.G_file, self.sites_filter_file)
        G_stacked = conv_stack(G, self.epochs)
        return G_stacked
        
    def get_d(self):
        disp = EpochalDisplacement(self.d_file, self.sites_filter_file)
        d = vstack_column_vec(disp, self.epochs)
        return d
        

    
