from numpy import log10

from .ed_sites_filtered import EDSitesFiltered
from .jacobian_vec import JacobianVec
from .formulate_occam import FormulatOccam
from .tikhonov_regularization import TikhonovSecondOrder
from .least_square import LeastSquare

class Inversion:
    def __init__(self):
        self.sites_file = 'sites'

        self.file_G1 = '../greensfunction/050km-vis02/G.h5'
        self.file_G2 = '../greensfunction/050km-vis01/G.h5'

        self.f_d = 'cumu_post.h5'

        self.f_slip0 = 'slip0.h5'

        self.epochs = []

        self.alpha = 100.

        self.file_pickled_raw_results = None
        
    def init(self):
        self.G1 = EDSitesFiltered(self.file_G1, self.sites_file)
        self.G2 = EDSitesFiltered(self.file_G2, self.sites_file)
        dG = DiffED(self.G1, self.G2, 'log10_visM')

        self.obs = EDSitesFiltered(self.f_d, self.sites_file)

        self.visM = self.G1.get_info('visM')
        self.log10_visM = log10(visM)
        print('Initial Maxwellian viscosity: %g'%visM)

        self.jac_1 = JacobianVec(dG, f_slip0)

        # FormulatOccam 
        self.formulate_occam = FormulatOccam()
        self.formulate_occam.epochs = self.epochs
        self.formulate_occam.non_lin_par_vals = [self.log10_visM]
        self.formulate_occam.non_lin_JacobianVecs = [self.jac_1]
        self.formulate_occam.G = self.G1
        self.formulate_occam.d = self.obs

        slef.d_ = self.formulate_occam.d_()
        self.jacobian = self.formulate_occam.Jacobian()

        # regularization
        self.reg = TikhonovSecondOrder(nrows_slip=10, ncols_slip=25)
        self.reg.row_norm_length = 1
        self.reg.col_norm_length = 28./23.03
        self.reg.num_epochs = len(self.epochs)
        self.reg.num_nlin_pars = 1

        # Inversion
        least_square = LeastSquare()
        least_square.G = jacobian
        least_square.d = d_
        least_square.alpha = alpha
        least_square.tikhonov_regularization = reg
        self.least_square = least_square

    def invert(self):
        self.solution = self.least_square()

        with open(self.file_pickled_raw_results,'wb') as fid:
            pickle.dump((self.alpha, self.solution),fid)

    def post_processing(self):
        pass
        
