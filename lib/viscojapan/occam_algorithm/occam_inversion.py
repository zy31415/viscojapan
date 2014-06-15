import pickle

from numpy import log10

from ..epochal_data.epochal_sites_data import EpochalG, EpochalDisplacement
from ..epochal_data.diff_ed import DiffED
from .jacobian_vec import JacobianVec
from .formulate_occam import FormulatOccam
from ..least_square.tikhonov_regularization import TikhonovSecondOrder
from ..least_square.least_square import LeastSquare


class OccamInversion:
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self):
        self.sites_file = ''

        self.file_G1 = ''
        self.file_G2 = ''

        self.f_d = ''

        self.f_slip0 = ''

        self.epochs = []

    def _formulate_occam(self):
        G1 = EpochalG(self.file_G1, self.sites_file)
        G2 = EpochalG(self.file_G2, self.sites_file)
        dG = DiffED(G1, G2, 'log10_visM')

        obs = EpochalDisplacement(self.f_d, self.sites_file)

        self.visM = G1.get_info('visM')
        self.log10_visM = log10(self.visM)
        print('Initial Maxwellian viscosity: %g'%self.visM)

        jac_1 = JacobianVec(dG, self.f_slip0)
        
        formulate_occam = FormulatOccam()
        formulate_occam.epochs = self.epochs
        formulate_occam.non_lin_par_vals = [self.log10_visM]
        formulate_occam.non_lin_JacobianVecs = [jac_1]
        formulate_occam.G = G1
        formulate_occam.d = obs
        return formulate_occam

    def _tikhonov_regularization(self):
        # regularization
        reg = TikhonovSecondOrder(nrows_slip=10, ncols_slip=25)
        reg.row_norm_length = 1
        reg.col_norm_length = 28./23.03
        reg.num_epochs = len(self.epochs)
        reg.num_nlin_pars = 1
        return reg

    def init(self):
        ''' The computation of the following three variable is quite time
cosuming. Because I need to do inversion for a series of alphas, I need to
pre-compute these three variable so that I don't need to compute them
everytime the alpha values changes.

Before. pickle this class, I need to delete these three variables, because
they take a lot memory and space.

jacobian
d_
tikhonov_regularization
'''
        formulate_occam = self._formulate_occam()
        
        self.jacobian = formulate_occam.Jacobian()
        self.d_ = formulate_occam.d_()
        self.tikhonov_regularization = self._tikhonov_regularization()
        

    def invert(self, alpha):
        least_square = LeastSquare()
        
        least_square.G = self.jacobian
        least_square.d = self.d_
        least_square.tikhonov_regularization = self.tikhonov_regularization
        
        least_square.alpha = alpha
        self.alpha =  alpha
        
        self.solution = least_square()

    def pickle(self,fn):
        self.jacobian = None
        self.d_ = None
        #self.tikhonov_regularization = None
        
        with open(fn, 'wb') as fid:
            pickle.dump(self, fid)

        
