import numpy as np
from cvxopt import matrix, solvers

import scipy.sparse as sparse

from ..utils import assert_col_vec_and_get_nrow,\
     assert_square_array_and_get_nrow

class CvxoptQpWrapper(object):
    def __init__(self,*,
                 P,
                 q,
                 GG = None
                 ):
        self.P = P
        self.q = q
        self.GG = GG
        
        self._check_input()

    def _check_input(self):
        nrow_P = assert_square_array_and_get_nrow(self.P)
        nrow_q = assert_col_vec_and_get_nrow(self.q)
        assert  nrow_P == nrow_q
        self.nrow_P = nrow_P

        if self.GG is not None:
            assert self.GG.shape[1] == nrow_P


    def invert(self, nonnegative=True):
        # non-negative constraint
        if nonnegative:
            GG = -1.0 * sparse.identity(self.nrow_P, dtype='float')
            if self.GG is not None:
                GG = sparse.vstack([GG, self.GG])

            h = np.zeros((GG.shape[0], 1), dtype='float')

            self.solution = solvers.qp(matrix(self.P),matrix(self.q),
                                       matrix(GG.todense()),matrix(h))
        else:
            if self.GG is not None:
                self.GG = matrix(self.GG)

            self.solution = solvers.qp(
                matrix(self.P),
                matrix(self.q),
                G = self.GG
            )

    @classmethod
    def create_from_inversion_parameters_set(cls, inv_par_set):
        P, q = inv_par_set.gen_inputs_for_cvxopt_qp()
        obj = cls(P=P, q=q)
        obj.GG = inv_par_set.GG
        return obj
        
