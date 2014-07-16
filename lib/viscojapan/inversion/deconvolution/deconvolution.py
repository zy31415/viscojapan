from numpy import loadtxt

from ..least_square import LeastSquareWithRegularization
from ..epochal_data import EpochalG, EpochalDisplacement, EpochalDisplacementSD
from ..inv_res_writer import WriterDeconvolution

class Deconvolution(LeastSquareTik2):
    def __init__(self,
                 file_G,
                 file_d,
                 file_sd,
                 file_sites_filter,
                 epochs,
                 basis_mat,
                 reg_mats,
                 reg_pars,
                 reg_par_names,
                 file_output,
                 ):
        self.file_G = file_G
        self.file_d = file_d
        self.file_sd = file_sd
        self.file_sites_filter = file_sites_filter

        self.epochs = epochs

        self.Ls = reg_mats
        self.reg_pars = reg_pars
        self.reg_par_names = reg_par_names
        assert len(self.Ls) = len(self.reg_pars)
        assert len(self.Ls) = len(self.reg_par_names)

        self.file_output = file_output

        self.res_writer = WriterDeconvolution(self)

    def _get_G(self):
        G = EpochalG(self.file_G, self.file_sites_filter)
        G_stacked = G.conv_stack(self.epochs)
        return G_stacked

    def _get_d(self):
        disp = EpochalDisplacement(self.file_d, self.file_sites_filter)
        d = disp.vstack(self.epochs)
        return d

    def _get_sig(self):
        if self.file_sd is not None:
            sig = EpochalDisplacementSD(self.file_sd, self.file_sites_filter)
            sig_stacked = sig.vstack(self.epochs)
        else:
            sig_stacked = None
        return sig_stacked

    def _load_data(self):
        self.G = self._get_G()
        self.d = self._get_d()
        self.sig = self._get_sig()

    def get_filtered_sites(self):
        sites = loadtxt(self.file_sites_filter,'4a')
        return sites

    def create_least_square_object(self):
        self._load_data()
        self.lease_squre = LeastSquareWithRegularization(
            G = self.G,
            d = self.d,
            sig = self.sig,
            Ls = self.Ls,
            B = self.B)

    def invert(self):        
        self.create_least_square_object()
        ls = self.lease_squre        
        ls.invert(*self.reg_pars)
        ls.predict()

        self.reg_mag = ls.get_reg_mag()
        self.nres_weighted = ls.get_residual_norm_weighted()
        self.nres = ls.get_residual_norm()
        
##    def compute_L_curve(self):
##        if not exists(self.outs_dir):
##            makedirs(self.outs_dir)
##
##        for ano, alpha in enumerate(self.alphas):
##            for bno, beta in enumerate(self.betas):
##                self.invert(alpha, beta)
##                self.predict()
##                self.res_writer.save_results(join(self.outs_dir,
##                            'res_a%02d_b%02d.h5'%(ano,bno)))
##                self.res_writer.save_results_incr_slip(join(self.outs_dir,
##                            'incr_slip_a%02d_b%02d.h5'%(ano,bno)))
##                self.res_writer.save_results_slip(join(self.outs_dir,
##                            'slip_a%02d_b%02d.h5'%(ano,bno)))
##                self.res_writer.save_results_pred_disp(join(self.outs_dir,
##                            'pred_disp_a%02d_b%02d.h5'%(ano,bno)))
        


