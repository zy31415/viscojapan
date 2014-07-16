import pickle
from os.path import exists

from numpy import log10, asarray, dot, loadtxt
import h5py

from ..epochal_data.epochal_sites_data import EpochalG, EpochalDisplacement
from ..epochal_data.diff_ed import DiffED
from .formulate_occam import JacobianVec, Jacobian, D_

from ..inv_res_writer import WriterOccamInversion
from ..deconvolution_inversion import Deconvolution

class OccamInversion():
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self,
                 file_G1,
                 file_G2,
                 file_d,
                 file_sd,
                 file_slip0,
                 file_sites_filter,
                 epochs,
                 nlin_par_initial_values,
                 nlin_par_names,
                 regularization,
                 basis,
                 ):
        
        self.file_G1 = file_G1
        self.file_G2 = file_G2
        self.file_d = file_d
        self.file_slip0 = file_slip0
        self.file_sites_filter = file_sites_filter
        self.epochs = epochs

        self.nlin_par_initial_values = nlin_par_initial_values
        self.nlin_par_names = nlin_par_names

        super().__init__(
            regularization,
            basis_matrix,)

    def iterate_nlin_par_name_val(self):
        for name, val in zip(self.nlin_par_names, self.nlin_par_initial_values):
            yield name, val        

    def init(self):
        assert len(self.nlin_par_initial_values) == len(self.nlin_par_names), \
               'Non-linear parameters setting inconsistancy.'
        self.num_nlin_pars = len(self.nlin_par_initial_values)

        for name, val in self.iterate_nlin_par_name_val():
            setattr(self, name,val)

        self._init_jacobian_vecs()

    def _init_jacobian_vecs(self):
        self.G1 = EpochalG(self.file_G1, self.sites_filter_file)
        G2 = EpochalG(self.file_G2, self.sites_filter_file)
        dG = DiffED(self.G1, G2, 'log10_visM')

        jac_1 = JacobianVec(dG, self.file_slip0)

        jacobian_vecs = [jac_1]

        self.jacobian_vecs = jacobian_vecs
        
    def _get_jacobian(self):
        jacobian = Jacobian()
        jacobian.G = self.G1
        jacobian.jacobian_vecs = self.jacobian_vecs
        jacobian.epochs = self.epochs
        jacobian_mat = jacobian()
        return jacobian_mat
        
    def _load_d_(self):
        d_ = D_()
        d_.jacobian_vecs = self.jacobian_vecs
        d_.nlin_par_values = self.nlin_par_initial_values
        d_.epochs = self.epochs

        obs = EpochalDisplacement(self.file_d, self.sites_filter_file)
        d_.d = obs
        d__vec = d_()
        return d__vec

    def set_G(self):
        self.G = self._get_jacobian()

    def set_d(self):
        self.d = self._load_d_()

    def set_data_sd(self):
        sig_ep = EpochalDisplacementSD(self.file_sd, self.file_sites_filter)
        self.sd = sig_ep(0)
        _assert_column_vector(self.sd)
        
    def predict(self):
        m = self.m
        G = self.G
        num_nlin_pars = self.num_nlin_pars
        assert num_nlin_pars > 0
        npars0 = asarray(self.nlin_par_initial_values)

        G1 = G[:,:-num_nlin_pars]
        G2 = G[:,-num_nlin_pars:]
        
        slip = m[:-num_nlin_pars]
        npars = m[-num_nlin_pars:]

        d = dot(G1,slip)

        delta_d = dot(G2, npars - npars0)

        d = d+delta_d

        d = d.reshape([-1,1])

        self.d_pred = d
