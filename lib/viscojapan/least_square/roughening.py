from scipy.sparse import eye, bmat, block_diag, coo_matrix, vstack
from numpy import sqrt

from ..utils import overrides

from .regularization import Regularization

# define functions
def roughening_matrix(num_cols):
        ''' Return any size of roughening matrix.
'''
        A = eye(num_cols-2, num_cols, k=0, dtype='float')
        B = -2. * eye(num_cols-2, num_cols, k=1, dtype='float')
        C = eye(num_cols-2, num_cols, k=2, dtype='float')
        return A+B+C

def finite_difference_matrix(num_cols):
        A = -1. * eye(num_cols-1, num_cols, k=0, dtype='float')
        B = eye(num_cols-1, num_cols, k=1, dtype='float')
        C = A + B
        return C

# define classes
class RowRoughening(Regularization):
    def __init__(self,
                 ncols_slip,
                 nrows_slip):
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        
    def row_roughening(self):
        ''' Roughening between rows.
'''
        A = eye(self.ncols_slip, dtype='float')
        B = -2. * eye(self.ncols_slip, dtype='float')

        block = []
        for nth in range(0, self.nrows_slip-2):
            block.append([None]*self.nrows_slip)
        
        for n in range(0,self.nrows_slip-2):
            block[n][n] = A
        for n in range(0,self.nrows_slip-2):
            block[n][n+1] = B
        for n in range(0,self.nrows_slip-2):
            block[n][n+2] = A

        mat = bmat(block, dtype='float')
        return mat
    
    def generate_regularization_matrix(self):
        return self.row_roughening()

class ColRoughening(Regularization):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip

    def col_roughening(self):
        ''' Roughening between columns.
'''
        mat = roughening_matrix(self.ncols_slip)
        mat = block_diag([mat]*self.nrows_slip)
        return mat

    def generate_regularization_matrix(self):
        return self.col_roughening()

class RowColRoughening(Regularization):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip

    def row_col_roughening(self):
        B = finite_difference_matrix(self.ncols_slip)
        A = -B

        block = []
        for nth in range(0, self.nrows_slip-1):
            block.append([None]*self.nrows_slip)
            
        for n in range(0,self.nrows_slip-1):
            block[n][n] = A
        for n in range(0,self.nrows_slip-1):
            block[n][n+1] = B
        mat =  bmat(block, dtype='float')  
        return mat

    def generate_regularization_matrix(self):
        return self.row_col_roughening()

class Roughening(Regularization):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 col_norm_length,
                 row_norm_length,
                 ):

        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        self.col_norm_length = col_norm_length
        self.row_norm_length = row_norm_length

    def generate_regularization_matrix(self):
        row = RowRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip)
        
        col = ColRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip)
        
        row_col = RowColRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip)

        row_mat = row()/(self.row_norm_length**2)
        col_mat = col()/(self.col_norm_length**2)
        row_col_mat = row_col()/(self.row_norm_length*self.col_norm_length)
        
        res = vstack([row_mat, col_mat, sqrt(2) * row_col_mat])
        
        return res

        
        

