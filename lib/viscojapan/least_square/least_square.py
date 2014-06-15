from numpy import zeros, dot, nan, identity
from cvxopt import matrix, solvers

class LeastSquare(object):
    def __init__(self):
        self.G = None
        self.d = None
        self.alpha = None
        self.tikhonov_regularization = None

    def __call__(self):
        G = self.G
        d = self.d
        npar = G.shape[1]

        self.regularization_matrix =\
            self.tikhonov_regularization.regularization_matrix()
        
        P = dot(G.T,G) + (self.alpha**2) * self.regularization_matrix
        
        q = -dot(G.T,d)

        # non-negative constraint
        GG = -1.0 * identity(npar, dtype='float')
        h = zeros((npar,1), dtype='float')
        
        sol = solvers.qp(matrix(P),matrix(q),
                         matrix(GG),matrix(h))

        return sol
