from scipy.sparse import coo_matrix

from viscojapan.fault_model import FaultFileIO
from ...utils import assert_nonnegative_integer, assert_assending_order

from .regularization import Leaf

def time_derivative_matrix(epochs):
    assert_assending_order(epochs)
    num_epochs = len(epochs)
    assert num_epochs >= 3, \
           'In order to compute time derivative, # of epochs must be equal or greater than 3.'

    nth_row = 0
    data = []
    I = []
    J = []
    for ith, epoch in enumerate(epochs[0:-1]):
        if epoch == 0:
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

class TemporalRegularization(Leaf):
    def __init__(self,
                 num_subflts,
                 epochs
                 ):
        self.num_subflts = num_subflts
        self.epochs = epochs

    def gen_inflated_time_derivative_mat(self):
        mat = time_derivative_matrix(self.epochs)
        res = inflate_time_derivative_matrix_by_num_subflts(mat, self.num_subflts)
        return res
        
    def generate_regularization_matrix(self):
        mat = self.gen_inflated_time_derivative_mat()
        return mat

    @staticmethod
    def create_from_fault_file(fault_file, epochs):
        fid = FaultFileIO(fault_file)
        num_subflts = fid.num_subflt_along_strike * fid.num_subflt_along_dip

        L = TemporalRegularization(
            num_subflts = num_subflts,
            epochs = epochs,
            )
        
        return L
