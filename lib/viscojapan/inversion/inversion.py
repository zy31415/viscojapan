import h5py
import numpy as np
import scipy.sparse as sparse

from .inversion_parameters_set import InversionParametersSet
from .cvxopt_qp_wrapper import CvxoptQpWrapper
from ..utils import delete_if_exists
from .result_file.result_file_writer import ResultFileWriter

class Inversion(object):
    def __init__(self,
                 regularization = None,
                 basis = None,
                 ):
        self.regularization = regularization
        self.basis = basis

    def set_data_sd(self):
        print('Set data sd ...')
        
    def set_data_W(self):
        print('Set data W ...')
        _sd = self.sd / np.median(self.sd)
        self.W = sparse.diags(1./_sd.flatten(), offsets=0)        

    def set_data_G(self):
        print('Set data G ...')               

    def set_data_d(self):
        print('Set data d ...') 

    def set_data_B(self):
        print('Set data B ...')
        self.B = self.basis()

    def set_data_L(self):
        print('Set data L ...')
        self.L = self.regularization()

    def set_data_Bm0(self):
        print("Set data Bm0 ...")
        self.Bm0 = None

    def set_data_all(self):
        self.set_data_sd()
        self.set_data_W()
        self.set_data_G()
        self.set_data_d()
        self.set_data_B()        
        self.set_data_L()
        self.set_data_Bm0()

    def set_data_except_L(self):
        self.set_data_sd()
        self.set_data_W()
        self.set_data_G()
        self.set_data_d()
        self.set_data_B()
        self.set_data_Bm0()

    def set_data_except(self, excepts):
        items = ['sd','W','G','d','B','L','Bm0']
        for item in excepts:
            items.remove(item)
        for item in items:
            getattr(self, 'set_data_%s'%item)()
        
    def invert(self, nonnegative=True):
        print('Inverting ...')

        self.inv_par_set = InversionParametersSet(
            G = self.G,
            d = self.d,
            W = self.W,
            B = self.B,
            L = self.L,
            Bm0 = self.Bm0)

        self.cvxopt_qp = CvxoptQpWrapper.\
                         create_from_inversion_parameters_set(self.inv_par_set)        
        self.cvxopt_qp.invert(nonnegative=nonnegative)
        
        self.m = np.asarray(self.cvxopt_qp.solution['x'],float).reshape((-1,1))
        self.Bm = self.B.dot(self.m)

    def predict(self):
        print('Predicting ...')        
        self.d_pred = np.dot(self.G, self.Bm)        

    def run(self):
        self.invert()
        self.predict()

    def get_residual_norm(self, subset=None):
        '''
return: ||G B m - d||
'''
        diff = self.d_pred - self.d
        if subset is not None:
            assert len(subset)==len(diff), 'subset length is smaller than diff'
            diff = diff[subset]
        return np.linalg.norm(diff)

    def get_residual_rms(self, subset=None):
        # note that self.disp_obs is different from self.d
        diff = (self.d_pred - self.disp_obs)
        if subset is not None:            
            assert len(subset)==len(diff), \
                   'subset length (%d) is smaller than that of diff (%d)'\
                   %(len(subset),len(diff))
            diff = diff[subset]
        return np.sqrt(np.mean(diff**2))

    def get_residual_norm_weighted(self):
        '''
return: ||W (G B m - d)||
'''
        res_w = self.W.dot(self.d_pred - self.d)
        nres_w = np.linalg.norm(res_w)
        return nres_w

    def save(self, fn, overwrite = False):
        print('Saving ...')
        if overwrite:
            delete_if_exists(fn)

        with ResultFileWriter(self, fn) as writer:
            writer.save()

        
        
    

        

        
