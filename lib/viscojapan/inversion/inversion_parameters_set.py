import warnings

import numpy as np
import scipy.sparse as sps

from ..utils import assert_col_vec_and_get_nrow

class InversionParametersSet(object):
    ''' Inversion parameters include the following parameters
showing in the following formula:
||W G B m - W d|| - ||L (B m + Bm0)||
W, G, B, m, d, L, Bm0
(m is the output)
'''
    def __init__(self,
                 G,
                 d,
                 W = None,
                 B = None,
                 L = None,
                 Bm0 = None
                 ):
        self.G = G
        self.d = d
        self.W = W
        self.B = B
        self.L = L
        self.Bm0 = Bm0

        self._check_input()

    def _check_input(self):
        self._check_type_and_get_shape_G()
        self._check_type_and_get_shape_d()
        self._check_type_and_get_shape_W()
        self._check_type_and_get_shape_B()
        self._check_type_and_get_shape_L()
        self._check_type_and_get_shape_Bm0()
        self._check_shape_for_matrix_operation()

    def _check_type_and_get_shape_G(self):
        assert isinstance(self.G, np.ndarray)
        self.nrow_G = self.G.shape[0]
        self.ncol_G = self.G.shape[1]

        if self.nrow_G <= self.ncol_G:
            warnings.warn('''G matrix: row # <= col #.
This means the inversion problem is under-determined.''')

    def _check_type_and_get_shape_d(self):
        self.nrow_d = assert_col_vec_and_get_nrow(self.d)
        self.ncol_d = 1

    def _check_type_and_get_shape_W(self):
        if self.W is None:
            self.W = sps.eye(self.nrow_G, dtype=float)
        assert sps.isspmatrix(self.W)
        self.nrow_W = self.W.shape[0]
        self.ncol_W = self.W.shape[1]
        assert self.nrow_W == self.ncol_W, 'W should be square.'

    def _check_type_and_get_shape_B(self):
        if self.L is None:
            self.B = sps.eye(self.ncol_G, dtype=float)
        assert sps.isspmatrix(self.B)
        self.nrow_B = self.B.shape[0]
        self.ncol_B = self.B.shape[1]
        if self.nrow_B < self.ncol_B:
            warnings.warn('''B matrix: row # < col #.
This means Green's function for bases might not be accurate.
''')

    def _check_type_and_get_shape_L(self):
        if self.L is None:
            self.L = sps.csr_matrix((1, self.nrow_B), dtype=float)
        assert sps.isspmatrix(self.L)
        self.nrow_L = self.L.shape[0]
        self.ncol_L = self.L.shape[1]  

    def _check_type_and_get_shape_Bm0(self):
        if self.Bm0 is None:
            self.Bm0 = np.zeros([self.ncol_L, 1], dtype=float)
        self.nrow_Bm0 = assert_col_vec_and_get_nrow(self.Bm0)
        

    def _check_shape_for_matrix_operation(self):
        ''' Check shape for the following operation:
||W G B m - W d|| - ||L (B m + Bm0)||
'''
        # first term
        assert self.ncol_W == self.nrow_G
        assert self.ncol_G == self.nrow_B
        assert self.ncol_W == self.nrow_d

        # second term
        assert self.ncol_L == self.nrow_B
        assert self.nrow_B == self.nrow_Bm0
        
