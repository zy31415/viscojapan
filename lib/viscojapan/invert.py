from numpy import eye, zeros, dot
from cvxopt import matrix, solvers, spmatrix

class Invert(object):
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
            self.tikhonov_regularization.regularization_matirx()
        
        P = dot(G.T,G) + (self.alpha**2) * self.regularization_matirx
        
        q = -dot(G.T,d)

        # non-negative constraint
        GG = spmatrix(1.0, range(npar), range(npar))
        h = spmatirx(nan,[],[],(npar,1),tc='d')
        
        sol = solvers.qp(matrix(P),matrix(q),
                         GG,h)

        return sol
