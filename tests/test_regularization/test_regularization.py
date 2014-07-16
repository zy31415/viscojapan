import unittest
from os.path import join

from pylab import plt
from numpy import asarray

from viscojapan.inversion.regularization.roughening import \
     RowRoughening, ColRoughening, RowColRoughening, Roughening
from viscojapan.inversion.regularization import Composite
from viscojapan.inversion.regularization.temporal_regularization import \
     TemporalRegularization
from viscojapan.test_utils import MyTestCase

class Test_Regularization(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def plot_mat(self, mat, fn):
        plt.matshow(asarray(mat.todense()))
        plt.axis('equal')
        sh = mat.shape
        plt.gca().set_yticks(range(0,sh[0]))
        plt.gca().set_xticks(range(0,sh[1]))
        plt.grid('on')
        plt.colorbar()
        plt.savefig(join(self.outs_dir, fn))
        plt.close()
        
    def test_row_roughening(self):
        reg = RowRoughening(
            ncols_slip = 3,
            nrows_slip = 5
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'row_roughening_mat.png')

    def test_col_roughening(self):
        reg = ColRoughening(
            ncols_slip = 5,
            nrows_slip = 3
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'col_roughening_mat.png')

    def test_RowColRoughening(self):
        reg = RowColRoughening(
            ncols_slip = 5,
            nrows_slip = 3
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'row_col_roughening_mat.png')

    def test_roughening(self):
        reg = Roughening(
            ncols_slip = 5,
            nrows_slip = 4,
            norm_length_strike = 1,
            norm_length_dip = 1,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'roughening_mat.png')

    def test_TemporalRegularization(self):
        reg = TemporalRegularization(
            num_subflts = 4,
            epochs = [1, 2, 5]
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'temporal_reg_mat.png')



        
if __name__ == '__main__':
    unittest.main()
