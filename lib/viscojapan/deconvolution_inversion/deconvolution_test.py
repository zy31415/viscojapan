from os.path import join, exists
from os import makedirs

from .deconvolution import Deconvolution
from ..inversion_test import gen_error_for_sites

class DeconvolutionTestFromFakeObs(Deconvolution):
    def __init__(self):
        super().__init__()
        self.num_err = None
        self.east_st = None
        self.north_st = None
        self.up_st = None

        self.outs_dir = None
        self.alphas = None
        self.betas = None

    def _get_d(self):
        d = super()._get_d()        
        err = gen_error_for_sites(self.num_err,
                                  self.east_st, self.north_st, self.up_st)
        d += err
        return d

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
                    
        
