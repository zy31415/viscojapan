from scipy.sparse import block_diag, bmat, eye, block_diag, coo_matrix, hstack

def hstack_zeros_padding(mat, num_cols):
    ''' Add zeros columns for non linear parameters
'''
    sh = mat.shape
    padding = coo_matrix((sh[0], num_cols),dtype='float')
    mat = hstack([mat,padding])
    return mat

class TikhonovRegularization:
    ''' Base class defines the interface.
'''
    def __init__(self):
        pass

    def regularization_matrix_each_epoch(self):
        ''' Return regularization matrix
'''
        raise NotImplementedError("Implement this function.")

    def regularization_matrix(self):
        mat = self.regularization_matrix_each_epoch()
        blocks = [mat]*self.num_epochs
        mat = block_diag(blocks, dtype = 'float')
        mat = hstack_zeros_padding(mat, self.num_nlin_pars)
        return mat

class TikhonovZerothOrder(TikhonovRegularization):
    def __init__(self, nrows_slip, ncols_slip):
        super().__init__()
        self.nrows_slip = nrows_slip
        self.ncols_slip = ncols_slip
        self.num_epochs = None
        
    def regularization_matrix_each_epoch(self):
        return eye(self.nrows_slip * self.ncols_slip, dtype='float')
    
class TikhonovSecondOrder(TikhonovRegularization):
    def __init__(self, nrows_slip, ncols_slip):
        super().__init__()
        self.nrows_slip = nrows_slip
        self.ncols_slip = ncols_slip
        self.row_norm_length = None
        self.col_norm_length = None
        self.num_epochs = None
        self.num_nlin_pars = None

    def roughening_matrix(self, num_cols):
        ''' Return any size of roughening matrix.
'''
        A = eye(num_cols-2, num_cols, k=0, dtype='float')
        B = -2. * eye(num_cols-2, num_cols, k=1, dtype='float')
        C = eye(num_cols-2, num_cols, k=2, dtype='float')
        return A+B+C
        
    def row_roughening(self):
        ''' Roughening between rows.
'''
        mat = self.roughening_matrix(self.nrows_slip)
        
        return block_diag([mat]*self.ncols_slip)

    def row_roughening_normed(self):
        return self.row_roughening() / (self.row_norm_length**2)


    def col_roughening(self):
        ''' Roughening between columns.
'''
        A = eye(self.nrows_slip, dtype='float')
        B = -2. * eye(self.nrows_slip, dtype='float')
        block = []
        for nth in range(0, self.ncols_slip-2):
            block.append([None]*self.ncols_slip)
        
        for n in range(0,self.ncols_slip-2):
            block[n][n] = A
        for n in range(0,self.ncols_slip-2):
            block[n][n+1] = B
        for n in range(0,self.ncols_slip-2):
            block[n][n+2] = A
        return bmat(block, dtype='float')

    def col_roughening_normed(self):
        return self.col_roughening() / (self.col_norm_length**2)

    def finite_difference_matrix(self, num_cols):
        A = -1. * eye(num_cols-1, num_cols, k=0, dtype='float')
        B = eye(num_cols-1, num_cols, k=1, dtype='float')
        C = A + B
        return C
        
    def row_col_roughening(self):
        B = self.finite_difference_matrix(self.nrows_slip)
        A = -B
        A, B
        block = []
        for nth in range(0, self.ncols_slip-1):
            block.append([None]*self.ncols_slip)
        for n in range(0,self.ncols_slip-1):
            block[n][n] = A
        for n in range(0,self.ncols_slip-1):
            block[n][n+1] = B
        return bmat(block, dtype='float')

    def row_col_roughening_normed(self):
        return self.row_col_roughening() / self.row_norm_length / self.col_norm_length

    def regularization_matrix_unnormed(self):
        row = self.row_roughening()
        col = self.col_roughening()
        row_col = self.row_col_roughening()

        return row.T.dot(row) + col.T.dot(col) +row_col.T.dot(row_col)
    
    def regularization_matrix_each_epoch(self):
        row = self.row_roughening_normed()
        col = self.col_roughening_normed()
        row_col = self.row_col_roughening_normed()

        return row.T.dot(row) + col.T.dot(col) +row_col.T.dot(row_col)


        
    
        
        
        
