from numpy import zeros, dot, nan, identity
from cvxopt import matrix, solvers

from .tikhonov_regularization import TikhonovSecondOrder

class LeastSquare(object):
    def __init__(self):
        pass

    def get_G(self):
        raise NotImplementedError("get_G")

    def get_d(self):
        raise NotImplementedError("get_d")

    def get_reg_mat(self):
        raise NotImplementedError("get_reg_mat")

    def load_data(self):
        self.G = self.get_G()
        self.d = self.get_d()
        self.reg_mat = self.get_reg_mat()

    def invert(self, alpha):
        G = self.G
        d = self.d
        npar = G.shape[1]
        
        P = dot(G.T,G) + (alpha**2) * self.reg_mat
        
        q = -dot(G.T,d)

        # non-negative constraint
        GG = -1.0 * identity(npar, dtype='float')
        h = zeros((npar,1), dtype='float')
        
        sol = solvers.qp(matrix(P),matrix(q),
                         matrix(GG),matrix(h))

        return sol

class LeastSquareTik2(LeastSquare):
    def __init__(self):
        super().__init__()
        self.num_epochs = None
        self.num_nlin_pars = None
        
    def get_reg_mat(self):
        # regularization
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = self.num_epochs
        tik.num_nlin_pars = self.num_nlin_pars
        
        self.tik_obj = tik
        reg_mat = tik()
        return reg_mat
    
