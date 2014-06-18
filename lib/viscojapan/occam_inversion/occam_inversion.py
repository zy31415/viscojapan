import pickle
from os.path import exists

from numpy import log10, asarray
import h5py

from ..epochal_data.epochal_sites_data import EpochalG, EpochalDisplacement
from ..epochal_data.diff_ed import DiffED
from ..epochal_data.stacking import break_col_vec_into_epoch_file
from ..least_square import LeastSquareTik2
from .formulate_occam import JacobianVec, Jacobian, D_
from ..utils import _assert_not_exists, overrides

class OccamInversionTik2(LeastSquareTik2):
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self):
        self.sites_file = ''

        self.file_G1 = ''
        self.file_G2 = ''

        self.f_d = ''

        self.f_slip0 = ''

        self.epochs = []

        self.nlin_par_values = [None]
        self.nlin_par_names = ['log10_visM']

    def init(self):

        assert len(self.nlin_par_values) == len(self.nlin_par_names), \
               'Non-linear parameters setting inconsistancy.'
        self.num_nlin_pars = len(self.nlin_par_values)

        self.num_epochs = len(self.epochs)
        self._init_jacobian_vecs()

    def _init_jacobian_vecs(self):
        self.G1 = EpochalG(self.file_G1, self.sites_file)
        G2 = EpochalG(self.file_G2, self.sites_file)
        dG = DiffED(self.G1, G2, 'log10_visM')

        jac_1 = JacobianVec(dG, self.f_slip0)

        jacobian_vecs = [jac_1]

        self.jacobian_vecs = jacobian_vecs
        

    def _get_jacobian(self):
        jacobian = Jacobian()
        jacobian.G = self.G1
        jacobian.jacobian_vecs = self.jacobian_vecs
        jacobian.epochs = self.epochs
        jacobian_mat = jacobian()
        return jacobian_mat

    @overrides(LeastSquareTik2)
    def load_G(self):
        return self._get_jacobian()
        
    def _get_d_(self):
        d_ = D_()
        d_.jacobian_vecs = self.jacobian_vecs
        d_.nlin_par_values = self.nlin_par_values
        d_.epochs = self.epochs

        obs = EpochalDisplacement(self.f_d, self.sites_file)
        d_.d = obs
        d__vec = d_()
        return d__vec

    @overrides(LeastSquareTik2)
    def load_d(self):
        return self._get_d_()

