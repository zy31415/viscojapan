from numpy import eye, zeros, dot
from cvxopt import matrix, solvers

class Invert(object):
    def __init__(self):
        self.G = None
        self.d = None
        self.alpha = None

    def __call__(self):
        G = self.G
        d = self.d

        npar = G.shape[1]
        I = eye(npar)
        I[-1,-1] = 0.

        _P = dot(G.T,G) + self.alpha**2*I
        P = matrix(_P)

        _q = -dot(G.T,d)
        q = matrix(_q)

        _GG = -I
        GG = matrix(_GG)

        _h = zeros(npar)
        h = matrix(_h)
        sol = solvers.qp(P,q,GG,h)

        return sol
