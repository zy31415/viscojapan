from scipy.sparse import eye, bmat, block_diag, coo_matrix, vstack
import scipy.sparse as sparse
from numpy import sqrt

from viscojapan.fault_model import FaultFileIO
from .regularization import Leaf, Composite

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
class RowRoughening(Leaf):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 norm_length_dip = 1.):
        super().__init__()
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        self.norm_length_dip = norm_length_dip
        
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
        return self.row_roughening()/(self.norm_length_dip**2)

class ColRoughening(Leaf):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 norm_length_strike = 1.
                 ):
        super().__init__()
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        self.norm_length_strike = norm_length_strike

    def col_roughening(self):
        ''' Roughening between columns.
'''
        mat = roughening_matrix(self.ncols_slip)
        mat = block_diag([mat]*self.nrows_slip)
        return mat

    def generate_regularization_matrix(self):
        return self.col_roughening()/(self.norm_length_strike**2)

class RowColRoughening(Leaf):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 norm_length_strike = 1.,
                 norm_length_dip = 1.,             
                 ):
        super().__init__()
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        self.norm_length_strike = norm_length_strike
        self.norm_length_dip = norm_length_dip

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
        return self.row_col_roughening()\
               /self.norm_length_dip/self.norm_length_strike

class Roughening(Composite):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,                 
                 norm_length_dip,
                 norm_length_strike,                 
                 ):

        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip
        self.norm_length_dip = norm_length_dip
        self.norm_length_strike = norm_length_strike

        col = ColRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip,
            norm_length_strike = self.norm_length_strike)

        row = RowRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip,
            norm_length_dip = self.norm_length_dip)
        
        row_col = RowColRoughening(
            ncols_slip = self.ncols_slip,
            nrows_slip = self.nrows_slip,
            norm_length_strike = self.norm_length_strike,
            norm_length_dip = self.norm_length_dip)

        components = [col, row, row_col]
        args = [1., 1., sqrt(2)]
        arg_names = ['col_roughening','row_roughening','row_col_roughening']
        
        super().__init__(
                components = components,
                args = args,
                arg_names = arg_names)

    @staticmethod
    def create_from_fault_file(fault_file):
        fid = FaultFileIO(fault_file)
        
        L2 = Roughening(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            norm_length_strike = 1.,
            norm_length_dip = \
                fid.subflt_sz_dip/fid.subflt_sz_strike,
            )
        return L2

class ExpandForAllEpochs(Leaf):
    def __init__(self,
                 reg,
                 num_epochs):
        self.reg = reg
        self.num_epochs = num_epochs

    def generate_regularization_matrix(self):
        regmat = self.reg()
        L = sparse.block_diag([regmat]*self.num_epochs)
        return L
        
        
                
        

