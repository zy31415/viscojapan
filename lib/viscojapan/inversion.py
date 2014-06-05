import pickle

from numpy import log10

from .ed_sites_filtered import EDSitesFiltered
from .jacobian_vec import JacobianVec
from .formulate_occam import FormulatOccam
from .tikhonov_regularization import TikhonovSecondOrder
from .least_square import LeastSquare
from .diff_ed import DiffED

class Inversion:
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
        formulate_occam = FormulatOccam()
        formulate_occam.epochs = self.epochs
        formulate_occam.non_lin_par_vals = [self.log10_visM]
        formulate_occam.non_lin_JacobianVecs = [self.jac_1]
        formulate_occam.G = self.G1
        formulate_occam.d = self.obs
        self.formulate_occam = formulate_occam
        
    def init(self):
        self.G1 = EDSitesFiltered(self.file_G1, self.sites_file)
        self.G2 = EDSitesFiltered(self.file_G2, self.sites_file)
        self.dG = DiffED(self.G1, self.G2, 'log10_visM')

        self.obs = EDSitesFiltered(self.f_d, self.sites_file)

        self.visM = self.G1.get_info('visM')
        self.log10_visM = log10(self.visM)
        print('Initial Maxwellian viscosity: %g'%self.visM)

        self.jac_1 = JacobianVec(self.dG, self.f_slip0)

        self._formulate_occam()

        self.d_ = self.formulate_occam.d_()
        self.jacobian = self.formulate_occam.Jacobian()

        # regularization
        reg = TikhonovSecondOrder(nrows_slip=10, ncols_slip=25)
        reg.row_norm_length = 1
        reg.col_norm_length = 28./23.03
        reg.num_epochs = len(self.epochs)
        reg.num_nlin_pars = 1
        self.tikhonov_regularization = reg

        # Inversion
        least_square = LeastSquare()
        least_square.G = self.jacobian
        least_square.d = self.d_
        least_square.tikhonov_regularization = self.tikhonov_regularization
        self.least_square = least_square

    def invert(self, alpha):
        self.least_square.alpha = alpha
        self.solution = self.least_square()
    
    def save_raw(self, file_name):
        with open(file_name,'wb') as fid:
            pickle.dump((self.least_square.alpha, self.solution),fid)

    def post_processing(self):
        pass
        
