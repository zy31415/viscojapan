import unittest
from os.path import join

from pylab import plt
from numpy import asarray

from viscojapan.least_square.my_regularization import \
     SpatialTemporalReg
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

class TestSpatialTemporalReg(unittest.TestCase):
    def setUp(self):
        pass
        
    def test(self):
        reg = SpatialTemporalReg()
        reg.nrows_slip = 5
        reg.ncols_slip = 3
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.epochs = [0,1,2,5]
        reg.num_nlin_pars = 1

        self.reg = reg
        mat = self.reg(1., 1.)
        plot_mat(mat, 'spatial_temporal_reg_mat.png')

    @timeit
    def test_speed(self):
        reg = SpatialTemporalReg()
        reg.nrows_slip = 10
        reg.ncols_slip = 25
        reg.row_norm_length = 1.
        reg.col_norm_length = 28./23.03

        reg.epochs = [0, 1, 2, 3, 4, 5, 6, 9, 13, 19, 28,
                      40, 58, 83, 120, 174, 251, 364, 526,760,1100]
        reg.num_nlin_pars = 1

        mat = reg(1.0, 1.0)
        print(mat.shape)
        
if __name__=='__main__':
    unittest.main()

