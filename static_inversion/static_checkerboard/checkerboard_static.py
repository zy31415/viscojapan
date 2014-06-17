import sys

from numpy import dot, asarray, hstack
from numpy.random import normal

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.fault.checkerboard import gen_checkerboard_slip
from viscojapan.epochal_data.epochal_sites_data import EpochalG
from viscojapan.least_square.least_square import LeastSquare
from viscojapan.least_square.tikhonov_regularization \
     import TikhonovSecondOrder

class CheckerBoardStatic(object):
    def __init__(self):
        pass

    def _form_G(self):
        f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        epochal_G = EpochalG(f_G, 'sites')
        G = epochal_G.get_epoch_value(0)
        self.G = G

    def _form_fake_d(self):
        # generate observation 
        slip = gen_checkerboard_slip(25, 10, 2, 2)*5.

        m = slip.reshape((-1,1))

        d = dot(self.G,m)

        east_error = normal(0, 6e-3, (1300,1))
        north_error = normal(0, 6e-3, (1300,1))
        up_error = normal(0,20e-3,(1300,1))
        error = hstack((east_error, north_error, up_error))
        error_flat = error.flatten().reshape([-1,1])

        d += error_flat

        self.d = d
        
    def set_up(self):
        self._form_G()
        self._form_fake_d()
        # inversion:
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = 1
        tik.num_nlin_pars = 0

        lst = LeastSquare()
        lst.G = self.G
        lst.d = self.d
        lst.regularization_matrix = tik()

        self.lst = lst

    def __call__(self, alpha):
        self.lst.alpha = alpha
        solution = self.lst()

        return solution
