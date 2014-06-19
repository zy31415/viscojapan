import unittest
from os.path import join

from pylab import plt
from numpy import asarray

from viscojapan.least_square.regularization import \
     RowRoughening, ColRoughening, RowColRoughening,\
     time_derivative_matrix, inflate_time_derivative_matrix_by_num_subflts,\
     TemporalRegularization
from viscojapan.utils import get_this_script_dir, timeit

this_script_dir = get_this_script_dir(__file__)

def plot_mat(mat, fn):
    plt.matshow(asarray(mat.todense()))
    plt.axis('equal')
    sh = mat.shape
    plt.gca().set_yticks(range(0,sh[0]))
    plt.gca().set_xticks(range(0,sh[1]))
    plt.grid('on')
    plt.colorbar()
    plt.savefig(join(this_script_dir, fn))
    plt.close()

class TestRowRougheningMat(unittest.TestCase):
    def setUp(self):
        reg = RowRoughening()
        reg.nrows_slip = 5
        reg.ncols_slip = 3
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.num_epochs = 2
        reg.num_nlin_pars = 3

        self.reg = reg
        
    def test_row_roughening(self):
        reg_mat = self.reg.row_roughening()
        plot_mat(reg_mat, 'row_roughening_mat.png')

    def test_row_roughening_normed(self):
        reg_mat = self.reg.row_roughening_normed()
        plot_mat(reg_mat, 'row_roughening_mat_normed.png')

    def test_row_roughening_stacked(self):
        reg_mat = self.reg()
        plot_mat(reg_mat, 'row_roughening_mat_stacked.png')
        
class TestColRougheningMat(unittest.TestCase):
    def setUp(self):
        reg = ColRoughening()
        reg.nrows_slip = 3
        reg.ncols_slip = 5
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.num_epochs = 2
        reg.num_nlin_pars = 3

        self.reg = reg
        
    def test_col_roughening(self):
        reg_mat = self.reg.col_roughening()
        plot_mat(reg_mat, 'col_roughening_mat.png')

    def test_col_roughening_normed(self):
        reg_mat = self.reg.col_roughening_normed()
        plot_mat(reg_mat, 'col_roughening_mat_normed.png')
##
    def test_col_roughening_stacked(self):
        reg_mat = self.reg()
        plot_mat(reg_mat, 'col_roughening_mat_stacked.png')

class TestRowColRoughening(unittest.TestCase):
    def setUp(self):
        reg = RowColRoughening()
        reg.nrows_slip = 4
        reg.ncols_slip = 5
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.num_epochs = 2
        reg.num_nlin_pars = 3

        self.reg = reg
        
    def test_row_col_roughening(self):
        reg_mat = self.reg.row_col_roughening()
        plot_mat(reg_mat, 'row_col_roughening_mat.png')

    def test_row_col_roughening_normed(self):
        reg_mat = self.reg.row_col_roughening_normed()
        plot_mat(reg_mat, 'row_col_roughening_mat_normed.png')
##
    def test_rwo_col_roughening_stacked(self):
        reg_mat = self.reg()
        plot_mat(reg_mat, 'row_col_roughening_mat_stacked.png')

    @timeit
    def test_speed(self):
        reg = RowColRoughening()
        reg.nrows_slip = 10
        reg.ncols_slip = 25
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.num_epochs = 21
        reg.num_nlin_pars = 1

        mat = reg()

class TestTemporalRegularization(unittest.TestCase):
    def setUp(self):
        self.epochs = [0,1,3,5,10,20]
        self.num_subflts = 4
        self.num_nlin_pars  = 3

    def test_time_derivative_matrix(self):
        mat = time_derivative_matrix(self.epochs)
        plot_mat(mat, 'temporal_reg.png')

    def test_inflate_time_derivative_matrix_by_num_subflts(self):
        mat = time_derivative_matrix(self.epochs)
        mat = inflate_time_derivative_matrix_by_num_subflts(mat,
                                                            self.num_subflts)
        plot_mat(mat, 'temporal_reg_inflated.png')

    def test_TemporalRegularization(self):
        reg = TemporalRegularization()
        reg.epochs = self.epochs
        reg.num_subflts = self.num_subflts
        reg.num_nlin_pars = self.num_nlin_pars

        mat = reg()
        plot_mat(mat, 'temporal_reg_mat_final.png')

    @timeit
    def test_speed(self):
        reg = TemporalRegularization()
        reg.epochs = [0, 1, 2, 3, 4, 5, 6, 9, 13, 19, 28,
                      40, 58, 83, 120, 174, 251, 364, 526,760,1100]
        reg.num_subflts = 250
        reg.num_nlin_pars = 1

        mat = reg()
        
if __name__=='__main__':
    unittest.main()

