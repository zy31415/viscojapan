from scipy.sparse import block_diag, bmat, eye

class TikhonovSecondOrder:
    def __init__(self, nrows_slip, ncols_slip):
        self.nrows_slip = nrows_slip
        self.ncols_slip = ncols_slip
        self.row_norm_length = None
        self.col_norm_length = None

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
        return self.row_col_roughening_norm() / self.row_norm_length / self.col_norm_length

    def regularization_matrix(self):
        row = self.row_roughening()
        col = self.col_roughening()
        row_col = self.row_col_roughening()

        return row.T.dot(row) + col.T.dot(col) +row_col.T.dot(row_col)
        
    
        
        
        
