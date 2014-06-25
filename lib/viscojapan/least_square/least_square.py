from numpy import zeros, dot, identity, asarray, ones, median
from numpy.linalg import norm
from scipy.sparse import diags
from cvxopt import matrix, solvers

from .my_regularization import SpatialTemporalReg
from ..utils import overrides, _assert_column_vector

class LeastSquare(object):
    def __init__(self):
        self.G = None
        self.d = None
        self.L = None

        self.sig = None

    def _check_input(self):        
        sh_G = self.G.shape

        self.num_pars = sh_G[1]
        self.num_obs = sh_G[0]
        
        nrows_d = _assert_column_vector(self.d)
        
        assert self.num_obs == nrows_d, "Shape of G and d doesn't match."

        if self.sig is None:
            self.sig = ones(len(self.d))
        assert len(self.sig) == self.num_obs, "Shape of d and sig should match."
        
        sh_L = self.L.shape
        assert self.num_pars == sh_L[1], "Shape of G and L doesn't match"
        
    def _form_weighting_matrix(self):        
        self._sig = self.sig / median(self.sig)
        self.W = diags(1./self._sig, offsets=0)
        
    def invert(self):
        self._check_input()
        self._form_weighting_matrix()
        
        Gw = self.W.dot(self.G)
        dw = self.W.dot(self.d)
        
        P = dot(Gw.T,Gw) + self.L.T.dot(self.L)
        
        q = -dot(Gw.T,dw)

        # non-negative constraint
        GG = -1.0 * identity(self.num_pars, dtype='float')
        h = zeros((self.num_pars,1), dtype='float')
        
        self.solution = solvers.qp(matrix(P),matrix(q),
                         matrix(GG),matrix(h))
        self.m = asarray(self.solution['x'],float).reshape((-1,1))

    def predict(self):
        d_pred = dot(self.G, self.m)
        self.d_pred = d_pred

    def get_residual_norm(self):
        return norm(self.d_pred - self.d)

    def get_residual_norm_weighted(self):
        print(self.d_pred-self.d)
        print('*')
        print(self.W)
        res_w = self.W.dot(self.d_pred - self.d)
        nres_w = norm(res_w)
        return nres_w
    

class LeastSquareTik2(LeastSquare):
    def __init__(self):
        super().__init__()
        self.G = None
        self.d =None
        
        self.nrows_slip = 10
        self.ncols_slip = 25
        
        self.row_norm_length = 1.
        self.col_norm_length = 28./23.03

        self.epochs = [0]
        self.num_nlin_pars = 0

    def _get_reg_mat(self, alpha, beta):
        reg = SpatialTemporalReg()
        reg.nrows_slip = self.nrows_slip
        reg.ncols_slip = self.ncols_slip
        reg.row_norm_length = self.row_norm_length
        reg.col_norm_length = self.col_norm_length

        reg.epochs = self.epochs
        reg.num_nlin_pars = self.num_nlin_pars

        self.regularization_matrix = reg

        mat = reg(alpha=alpha, beta=beta)
        return mat

    @overrides(LeastSquare)    
    def invert(self, alpha, beta):        
        self.L = self._get_reg_mat(alpha, beta)
        self.solution = super().invert()
        self.alpha = alpha
        self.beta = beta

    def get_spatial_roughness(self):
        return self.regularization_matrix.get_spatial_roughness(self.m)

    def get_temporal_roughness(self):
        if len(self.epochs) < 3:
            raise ValueError('Two few epochs. Cannot compute temoral roughness.')        
        return self.regularization_matrix.get_temporal_roughness(self.m)

    def num_epochs(self):
        return len(self.epochs)
