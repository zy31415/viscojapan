from numpy import zeros, dot, identity, asarray, ones, ndarray
from numpy.linalg import norm
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.csr import csr_matrix
from cvxopt import matrix, solvers

from ..utils import _assert_column_vector

class LeastSquare(object):
    def __init__(self,
                 G,
                 d,
                 L = None,
                 W = None,
                 B = None,
                 Bm0 = None
                 ):
        self.G = G
        self.d = d
        self.L = L
        self.W = W
        self.B = B
        self.Bm0 = Bm0

        self._check_input()
            
    def _check_input(self):
        ''' Assert the following operation is possible:
||W G B m - W d|| - ||L (B m + B m0)||
W - sparse, weighting matrix
G - ndarray, green's function
B - sparse, basis matrix
L - sparse, regularization matrix
'''
        self.num_obs = _assert_column_vector(self.d)

        if self.W is None:
            self.W = sparse.eye(num_obs)
        else:
            assert self.W.shape[1] == self.G.shape[0]

        self.num_pars = self.B.shape[1]

        if self.B is None:
            self.B = sparse.eye(num_pars)
        else:
            self.G.shape[1] == self.B.shape[0]

        num_subflts = self.B.shape[0]
        if self.L is None:
            self.L = sparse.csr_matrix((1,num_subflts),dtype=float)
        else:
            assert self.L.shape[1] == num_subflts

        if self.Bm0 is None:
            self.Bm0 = zeros([self.num_pars, 1])
        else:
            assert self.Bm0.shape == (self.num_pars, 1)

        # assert type:
        self.W = csr_matrix(self.W)
        self.B = csr_matrix(self.B)
        self.L = csr_matrix(self.L)
        assert isinstance(self.G, ndarray)
        assert isinstance(self.Bm0, ndarray)
        
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
        
        q = - dot(WGB.T,Wd) - LB.T.dot(self.L).dot(self.Bm0)        

        # non-negative constraint
        if nonnegative:
            GG = -1.0 * identity(self.num_pars, dtype='float')
            h = zeros((self.num_pars,1), dtype='float')
            self.solution = solvers.qp(matrix(P),matrix(q),
                                       matrix(GG),matrix(h))
        else:
            self.solution = solvers.qp(matrix(P),matrix(q))
            
        self.m = asarray(self.solution['x'],float).reshape((-1,1))
        self.Bm = self.B.dot(self.m)

    def predict(self):
        '''
return: d_pred = G B m
'''
        d_pred = dot(self.G, self.Bm)
        self.d_pred = d_pred

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
        diff = self.d_pred - self.d
        if subset is not None:
            assert len(subset)==len(diff), 'subset length is smaller than diff'
            diff = diff[subset]
        return np.sqrt(np.mean(diff**2))

    def get_residual_norm_weighted(self):
        '''
return: ||W (G B m - d)||
'''
        res_w = self.W.dot(self.d_pred - self.d)
        nres_w = norm(res_w)
        return nres_w

##    def get_solution_norm(self):
##        '''
##return: ||L B m||
##'''
##        tp = self.L.dot(self.Bm + self.Bm0)
##        return dot(tp.T, tp)[0,0]
    
