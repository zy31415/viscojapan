from numpy import dot
import scipy.sparse as sparse

from .least_square import LeastSquare

class LeastSquareWithRegularization(LeastSquare):
    def __init__(self,
                 G,
                 d,
                 Ls,
                 sig = None,
                 B = None,
                 ):
        self.G = G
        self.d = d
        self.Ls = Ls
        self.sig = sig
        self.B = B
                

    def _gen_L(self, *args):
        assert len(args) == len(self.Ls)
        L_list = []
        for L, arg in zip(self.Ls, args):
            tp = sparse.csr_matrix(L)
            L_list.append(arg*tp)
        L_stack = sparse.vstack(L_list)
        return L_stack

    def invert(self, *args, nonnegative=True):
        L_stacked = self._gen_L(*args)
        super().__init__(
            G = self.G,
            d = self.d,
            L = L_stacked,
            sig = self.sig,
            B = self.B,
            )
        super().invert(nonnegative=nonnegative)

    def get_reg_mag(self):
        res = []
        for Li in self.Ls:
            tp = Li.dot(self.Bm)
            res.append(dot(tp.T, tp)[0,0])
        return res

        
        
        
