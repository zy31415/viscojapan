from scipy.sparse import eye, bmat, block_diag, coo_matrix, hstack

from ..utils import overrides, _assert_nonnegative_integer, _assert_assending_order

# define functions
def pad_zero_col(mat, n):
    ''' Add zeros columns and rows for non linear parameters
'''
    _assert_nonnegative_integer(n)
    if n==0:
        return mat
    
    # add zero cols
    sh = mat.shape
    col_padding = coo_matrix((sh[0], n),dtype='float')
    mat = hstack([mat, col_padding])
    
    return mat

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

def time_derivative_matrix(epochs):
    _assert_assending_order(epochs)
    num_epochs = len(epochs)
    assert num_epochs >= 3, \
           'In order to compute time derivative, # of epochs must be equal or greater than 3.'

    nth_row = 0
    data = []
    I = []
    J = []
    for ith, epoch in enumerate(epochs[0:-1]):
        if ith == 0:
            continue
        
        data += [-1./(epoch - epochs[ith-1]), 1./(epochs[ith+1] - epoch)]
        I    += [nth_row,  nth_row]
        J    += [ith, ith+1]
        
        nth_row += 1

    res = coo_matrix((data,(I,J)),dtype=float)
    return res

def inflate_time_derivative_matrix_by_num_subflts( time_derivative_mat, num_subflts):
    data0 = time_derivative_mat.data
    row0 = time_derivative_mat.row
    col0 = time_derivative_mat.col

    data = []
    row = []
    col = []
    for di, ri, ci in zip(data0, row0, col0):
        _data = [di]*num_subflts
        _row = [ri*num_subflts + ii for ii in range(num_subflts)]
        _col = [ci*num_subflts + ii for ii in range(num_subflts)]

        data += _data
        row += _row
        col += _col

    res = coo_matrix((data, (row, col)),dtype=float)
    return res
        

# define classes    
class Regularization(object):
    def __init__(self):
        pass
        
    def __call__(self):
        raise NotImplementedError(
            "This interface returns the regularization matrix.")

class SpatialRegularization(Regularization):
    def __init__(self):
        # fault geometry parameter
        self.nrows_slip = None
        self.ncols_slip = None
        self.row_norm_length = None
        self.col_norm_length = None
        
        self.num_epochs = None
        self.num_nlin_pars = None
        
    def regularization_matrix_each_epoch(self):
        raise NotImplementedError(
            "This interface returns spatial regularization matrix of each epoch.")

    def diagonal_stack(self):
        mat = self.regularization_matrix_each_epoch()
        blocks = [mat]*self.num_epochs
        mat = block_diag(blocks, dtype = 'float')
        return mat
        
    @overrides(Regularization)
    def __call__(self):
        mat = self.diagonal_stack()
        mat = pad_zero_col(mat, self.num_nlin_pars)
        return mat

class RowRoughening(SpatialRegularization):
    def __init__(self):
        super().__init__()
        
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

    def row_roughening_normed(self):
        return self.row_roughening() / (self.row_norm_length**2)

    @overrides(SpatialRegularization)
    def regularization_matrix_each_epoch(self):
        return self.row_roughening_normed()

class ColRoughening(SpatialRegularization):
    def __init__(self):
        super().__init__()

    def col_roughening(self):
        ''' Roughening between columns.
'''
        mat = roughening_matrix(self.ncols_slip)
        mat = block_diag([mat]*self.nrows_slip)
        return mat

    def col_roughening_normed(self):
        return self.col_roughening() / (self.col_norm_length**2)

    @overrides(SpatialRegularization)
    def regularization_matrix_each_epoch(self):
        return self.col_roughening_normed()

class RowColRoughening(SpatialRegularization):
    def __init__(self):
        super().__init__()

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

    def row_col_roughening_normed(self):
        return self.row_col_roughening() / self.row_norm_length / self.col_norm_length

    @overrides(SpatialRegularization)
    def regularization_matrix_each_epoch(self):
        return self.row_col_roughening_normed()

class TemporalRegularization(Regularization):
    def __init__(self):
        self.num_subflts = None
        self.epochs = None
        self.num_nlin_pars = None

    def gen_inflated_time_derivative_mat(self):
        mat = time_derivative_matrix(self.epochs)
        res = inflate_time_derivative_matrix_by_num_subflts(mat, self.num_subflts)
        return res
        
    @overrides(Regularization)
    def __call__(self):
        mat = self.gen_inflated_time_derivative_mat()
        res = pad_zero_col(mat, self.num_nlin_pars)
        return res
        
        
        

