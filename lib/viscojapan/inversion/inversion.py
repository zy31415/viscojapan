import h5py
from numpy import median 
import scipy.sparse as sparse

from .least_square import LeastSquare
from ..utils import delete_if_exists

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
        _sd = self.sd / median(self.sd)
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

    def invert(self, nonnegative=True):
        print('Inverting ...')
        
        self.least_square = LeastSquare(
            G = self.G,
            d = self.d,
            L = self.L,
            W = self.W,
            B = self.B,
            Bm0 = self.Bm0
            )

        self.least_square.invert(nonnegative=nonnegative)

    def predict(self):
        print('Predicting ...')
        self.least_square.predict()
        self.d_pred = self.least_square.d_pred

    def run(self):
        self.invert()
        self.predict()

    def get_residual_norm(self):
        return self.least_square.get_residual_norm()

    def get_residual_norm_weighted(self):
        return self.least_square.get_residual_norm_weighted()

    def save(self, fn, overwrite = False):
        print('Saving ...')
        if overwrite:
            delete_if_exists(fn)
        ls = self.least_square
        with h5py.File(fn) as fid:
            fid['m'] = ls.m
            fid['Bm'] = ls.Bm
            fid['d_pred'] = self.d_pred
            fid['residual_norm'] = self.get_residual_norm()
            fid['residual_norm_weighted'] = self.get_residual_norm_weighted()

            for par, name in zip(self.regularization.args,
                                 self.regularization.arg_names):
                fid['regularization/%s/coef'%name] = par
                
            for nsol, name in zip(self.regularization.components_solution_norms(ls.Bm),
                                  self.regularization.arg_names):
                fid['regularization/%s/norm'%name] = nsol

    

        

        
