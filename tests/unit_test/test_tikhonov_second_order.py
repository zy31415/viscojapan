import unittest
from os.path import join

from pylab import pcolor, savefig, close, colorbar, axis, asarray

from viscojapan.least_square.tikhonov_regularization \
     import TikhonovSecondOrder
from viscojapan.utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

class TestTikhonovSecondOrder(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_tik_mat_for_visinv(self):
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = 2
        tik.num_nlin_pars = 1
        tik_mat = tik()

##        pcolor(asarray(tik_mat.todense()))
##        colorbar()
##        axis('equal')
##        savefig(join(this_script_dir,'tik_mat_visinv.pdf'))
##        close()
        

    def test_tik_mat_for_coseismic_invertion(self):
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = 1
        tik.num_nlin_pars = 0
        tik_mat = tik()

##        pcolor(asarray(tik_mat.todense()))
##        colorbar()
##        axis('equal')
##        savefig(join(this_script_dir,'tik_mat_coseismic.pdf'))
##        close()


if __name__=='__main__':
    unittest.main()
