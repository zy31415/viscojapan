import h5py

from ..epochal_data import EpochalData, break_col_vec_into_epoch_file
from ..utils import _assert_nonnegative_integer, overrides

class InvResWriter(object):
    def __init__(self, inv):
        self.inv = inv        

class WriterLeastSquareTik2(InvResWriter):
    def __init__(self, inv):
        super().__init__(inv)

    def save_results(self, fn):
        with h5py.File(fn) as fid:
            fid['m'] = self.inv.m
            fid['d'] = self.inv.d
            fid['d_pred'] = self.inv.d_pred
            fid['roughness'] = self.inv.roughness()
            fid['residual_norm'] = self.inv.residual_norm()
            fid['alpha'] = self.inv.alpha

class WriterDeconvolution(WriterLeastSquareTik2):
    def __init__(self, inv):
        super().__init__(inv)

    @overrides(WriterLeastSquareTik2)
    def save_results(self, fn):
        super().save_results(fn)
        with h5py.File(fn) as fid:
            fid['num_nlin_pars'] = self.inv.num_nlin_pars
            fid['epochs'] = self.inv.epochs
            fid['num_epochs'] = self.inv.num_epochs
            fid['sites'] = self.inv.get_filtered_sites()

    def save_results_incr_slip(self, fn):
        _assert_nonnegative_integer(self.inv.num_nlin_pars)
        if self.inv.num_nlin_pars == 0:
            break_col_vec_into_epoch_file(self.inv.m, self.inv.epochs, fn)
        else:
            break_col_vec_into_epoch_file(self.inv.m[0:-self.inv.num_nlin_pars],
                                      self.inv.epochs, fn)

        EpochalData(fn).set_info('alpha', self.inv.alpha)

    def save_results_pred_disp(self, fn):
        info = {'sites':self.inv.get_filtered_sites()}
        break_col_vec_into_epoch_file(self.inv.d, self.inv.epochs, fn,
                                      info_dic = info)    
        
class WriterOccamInversion(WriterDeconvolution):
    def __init__(self, inv):
        super().__init__(inv)

    @overrides(WriterDeconvolution)
    def save_results(self, fn):
        super().save_results(fn)
        with h5py.File(fn) as fid:
            for name, val in self.inv.iterate_nlin_par_name_val():
                fid['nlin_par_initial_values/%s'%name] = val

        
