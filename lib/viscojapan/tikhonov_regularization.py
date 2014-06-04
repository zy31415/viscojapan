from scipy.sparse import block_diag, bmat, eye, block_diag, coo_matrix, hstack, vstack

def zeros_padding(mat, num_cols):
    ''' Add zeros columns and rows for non linear parameters
'''
    # add zero cols
    sh = mat.shape
    col_padding = coo_matrix((sh[0], num_cols),dtype='float')
    mat = hstack([mat, col_padding])

    # add zero rows
    sh = mat.shape
    row_padding = coo_matrix((sh[1], num_cols),dtype='float')
    mat = vstack([mat, row_padding])
    
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
        mat = zeros_padding(mat, self.num_nlin_pars)
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

    def col_roughening(self):
        ''' Roughening between columns.
'''
        mat = self.roughening_matrix(self.ncols_slip)
        mat = block_diag([mat]*self.nrows_slip)
        return mat 

    def col_roughening_normed(self):
        return self.col_roughening() / (self.col_norm_length**2)

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


    def finite_difference_matrix(self, num_cols):
        A = -1. * eye(num_cols-1, num_cols, k=0, dtype='float')
        B = eye(num_cols-1, num_cols, k=1, dtype='float')
        C = A + B
        return C

    def row_col_roughening(self):
        B = self.finite_difference_matrix(self.ncols_slip)
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

    def roughening_matrix_each_epoch(self):
        row = self.row_roughening_normed()
        col = self.col_roughening_normed()
        row_col = self.row_col_roughening_normed()

        return row.T.dot(row) + col.T.dot(col) +row_col.T.dot(row_col)

        
    
        
        
        
