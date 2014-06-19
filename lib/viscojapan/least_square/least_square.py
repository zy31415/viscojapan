from numpy import zeros, dot, identity, asarray
from numpy.linalg import norm
from cvxopt import matrix, solvers
       
class LeastSquare(object):
    def __init__(self):
        self.G = None
        self.d = None
        self.L = None

    def invert(self, alpha):
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
