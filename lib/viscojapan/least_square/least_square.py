from numpy import zeros, dot, nan, identity, asarray, sqrt
from numpy.linalg import norm
from cvxopt import matrix, solvers
import h5py

from .tikhonov_regularization import TikhonovSecondOrder
from ..utils import overrides
        
class LeastSquare(object):
    def __init__(self):
        pass

    def _load_G(self):
        raise NotImplementedError("get_G")

    def _load_d(self):
        raise NotImplementedError("get_d")

    def _load_reg_mat(self):
        raise NotImplementedError("get_reg_mat")

    def load_data(self):
        self.G = self._load_G()
        self.d = self._load_d()
        self.reg_mat = self._load_reg_mat()

    def _least_square(self, alpha):
        G = self.G
        d = self.d
        npar = G.shape[1]
        
        P = dot(G.T,G) + (alpha**2) * self.reg_mat
        
        q = -dot(G.T,d)

        # non-negative constraint
        GG = -1.0 * identity(npar, dtype='float')
        h = zeros((npar,1), dtype='float')
        
        self.solution = solvers.qp(matrix(P),matrix(q),
                         matrix(GG),matrix(h))
        self.m = asarray(self.solution['x'],float).reshape((-1,1))
        self.alpha = alpha

    def _predict(self):
        d_pred = dot(self.G, self.m)
        self.d_pred = d_pred

    def invert(self, alpha):
        self._least_square(alpha)
        self._predict()        

class LeastSquareTik2(LeastSquare):
    def __init__(self):
        super().__init__()
        self.num_epochs = None
        self.num_nlin_pars = None

    @overrides(LeastSquare)
    def _load_reg_mat(self):
        # regularization
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = self.num_epochs
        tik.num_nlin_pars = self.num_nlin_pars
        
        self.tik_obj = tik
        self.reg_mat = tik()
        return self.reg_mat

    def roughness_square(self):
        rough = dot(self.m.T, self.reg_mat.dot(self.m))[0,0]
        return rough

    def roughness(self):
        return sqrt(self.roughness_square())

    def residual_norm(self):
        nres = norm(self.d -self.d_pred)
        return nres

    def save_results(self, fn):
        with h5py.File(fn) as fid:
            fid['m'] = self.m
            fid['d'] = self.d
            fid['d_pred'] = self.d_pred
            fid['roughness'] = self.roughness()
            fid['residual_norm'] = self.residual_norm()
            fid['alpha'] = self.alpha
        
    
