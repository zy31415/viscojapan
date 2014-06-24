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

        self.outs_dir = None
        self.alphas = None
        self.betas = None

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

    def compute_L_curve(self):
        if not exists(self.outs_dir):
            makedirs(self.outs_dir)

        for ano, alpha in enumerate(self.alphas):
            for bno, beta in enumerate(self.betas):
                self.invert(alpha, beta)
                self.predict()
                self.res_writer.save_results(join(self.outs_dir,
                            'res_a%02d_b%02d.h5'%(ano,bno)))
                self.res_writer.save_results_incr_slip(join(self.outs_dir,
                            'incr_slip_a%02d_b%02d.h5'%(ano,bno)))
                self.res_writer.save_results_slip(join(self.outs_dir,
                            'slip_a%02d_b%02d.h5'%(ano,bno)))
                self.res_writer.save_results_pred_disp(join(self.outs_dir,
                            'pred_disp_a%02d_b%02d.h5'%(ano,bno)))
        


