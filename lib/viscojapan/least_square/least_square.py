from numpy import zeros, dot, identity, asarray, ones, median, ndarray
from numpy.linalg import norm
import scipy.sparse as sparse
from scipy.sparse.csr import csr_matrix
from cvxopt import matrix, solvers

from ..utils import overrides, _assert_column_vector

class LeastSquare(object):
    def __init__(self,
                 G,
                 d,
                 L,
                 sig = None,
                 B = None,
                 ):
        self.G = G
        self.d = d
        self.L = L
        self.sig = sig
        self.B = B

        self._check_input()

    def _check_input(self):
        ''' Assert the following operation is possible:
||W G B m - W d|| - ||L B m||
W - sparse
G - not sparse
B - sparse
L - sparse
'''
        self.num_obs = _assert_column_vector(self.d)

        if self.sig is None:
            self.sig = ones([self.num_obs, 1])
        len_sig = _assert_column_vector(self.sig)
        assert len_sig == self.num_obs
        self._form_weighting_matrix()

        assert self.W.shape[1] == self.G.shape[0]

        if self.B is None:
            num_pars = self.G.shape[1]
            self.B = sparse.eye(num_pars)

        self.num_pars = self.B.shape[1]
            
        assert self.G.shape[1] == self.B.shape[0]

        assert self.L.shape[1] == self.B.shape[0]

        # assert type:
        self.W = csr_matrix(self.W)
        self.B = csr_matrix(self.B)
        self.L = csr_matrix(self.L)
        assert isinstance(self.G, ndarray)
        
        
    def _form_weighting_matrix(self):        
        self._sig = self.sig / median(self.sig)
        self.W = sparse.diags(1./self._sig.flatten(), offsets=0)
        
    def invert(self, nonnegative=True):
        ''' Solve the problem:
||W G B m - W d|| - ||L B m||
'''
        WG = self.W.dot(self.G)
        assert isinstance(WG, ndarray)
        WGB = csr_matrix.dot(WG, self.B)
        
        Wd = self.W.dot(self.d)
        
        LB = self.L.dot(self.B)
        
        P = dot(WGB.T,WGB) + LB.T.dot(LB)
        
        q = -dot(WGB.T,Wd)

        # non-negative constraint
        if nonnegative:
            GG = -1.0 * identity(self.num_pars, dtype='float')
            h = zeros((self.num_pars,1), dtype='float')
            self.solution = solvers.qp(matrix(P),matrix(q),
                                       matrix(GG),matrix(h))
        else:
            self.solution = solvers.qp(matrix(P),matrix(q))
            
        self.m = asarray(self.solution['x'],float).reshape((-1,1))

    def predict(self):
        d_pred = dot(self.G, self.B.dot(self.m))
        self.d_pred = d_pred

    def get_residual_norm(self):
        return norm(self.d_pred - self.d)

    def get_residual_norm_weighted(self):
        res_w = self.W.dot(self.d_pred - self.d)
        nres_w = norm(res_w)
        return nres_w
    
