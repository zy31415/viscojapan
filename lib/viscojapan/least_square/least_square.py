from numpy import zeros, dot, identity, asarray
from numpy.linalg import norm
from cvxopt import matrix, solvers

from .my_regularization import SpatialTemporalReg
from ..utils import overrides

class LeastSquare(object):
    def __init__(self):
        self.G = None
        self.d = None
        self.L = None

    def invert(self):
        G = self.G
        d = self.d
        npar = G.shape[1]
        
        P = dot(G.T,G) + self.L.T.dot(self.L)
        
        q = -dot(G.T,d)

        # non-negative constraint
        GG = -1.0 * identity(npar, dtype='float')
        h = zeros((npar,1), dtype='float')
        
        self.solution = solvers.qp(matrix(P),matrix(q),
                         matrix(GG),matrix(h))
        self.m = asarray(self.solution['x'],float).reshape((-1,1))

    def predict(self):
        d_pred = dot(self.G, self.m)
        self.d_pred = d_pred

    def get_residual_norm(self):
        return norm(self.d_pred -  self.d)        

class LeastSquareTik2(LeastSquare):
    def __init__(self):
        super().__init__()
        self.G = None
        self.d =None
        
        self.nrows_slip = 10
        self.ncols_slip = 25
        
        self.row_norm_length = 1.
        self.col_norm_length = 28./23.03

        self.epochs = None
        self.num_nlin_pars = None

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
