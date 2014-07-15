from os.path import exists, join
from os import makedirs

class LCurve(object):
    def __init__(self, inv_obj):
        self.inv_obj = inv_obj
        
        self.alphas = None
        self.betas = None
        self.outs_dir = None
    
    def compute_L_curve(self):
        inv_obj = self.inv_obj
        if not exists(self.outs_dir):
            makedirs(self.outs_dir)

        for ano, alpha in enumerate(self.alphas):
            for bno, beta in enumerate(self.betas):
                inv_obj.invert(alpha, beta)
                inv_obj.predict()
                inv_obj.res_writer.save_results(join(self.outs_dir,
                            'res_a%02d_b%02d.h5'%(ano,bno)))
                inv_obj.res_writer.save_results_incr_slip(join(self.outs_dir,
                            'incr_slip_a%02d_b%02d.h5'%(ano,bno)))
                inv_obj.res_writer.save_results_slip(join(self.outs_dir,
                            'slip_a%02d_b%02d.h5'%(ano,bno)))
                inv_obj.res_writer.save_results_pred_disp(join(self.outs_dir,
                            'pred_disp_a%02d_b%02d.h5'%(ano,bno)))
