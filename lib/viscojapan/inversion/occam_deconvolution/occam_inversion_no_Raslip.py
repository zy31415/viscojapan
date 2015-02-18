import numpy as np
import scipy.sparse as sparse

from ..epoch_file_reader_for_inversion import EpochG, DifferentialG, EpochDisplacement, EpochDisplacementSD, \
    EpochSlip

from .formulate_occam import JacobianVec, Jacobian, D_
from ..inversion import Inversion
from ...sites_db import choose_inland_GPS_cmpts_for_all_epochs

from ..regularization.temporal_regularization import time_derivative_matrix, inflate_time_derivative_matrix_by_num_subflts

from .occam_deconvolution import OccamDeconvolution

__all__ = ['OccamInversionNoRaslip']


class OccamInversionNoRaslip(OccamDeconvolution):
    def __init__(self,
                 file_G0,
                 files_Gs,
                 nlin_par_names,
                 file_d,
                 file_sd,
                 sites,
                 epochs,                 
                 regularization,
                 basis,
                 file_slip0,
                 decreasing_slip_rate = True,
                 ):

        super().__init__(
            regularization,
            basis,)

        self.G0 = EpochG(file_G0, sites)
        self.num_subflts = self.G0.get_num_subflts()

        self.Gs = [EpochG(f, sites) for f in files_Gs]

        self.nlin_par_names = nlin_par_names
        
        self.d = EpochDisplacement(file_d, sites)

        self.sd = EpochDisplacementSD(file_sd, sites)

        self.epochs = epochs

        self.slip0 = EpochSlip(file_slip0).respace(self.epochs)
        self.num_subflt_along_dip = self.slip0.num_subflt_along_dip
        self.num_subflt_along_strike = self.slip0.num_subflt_along_strike

        self.sites = sites

        self.num_epochs = len(self.epochs)

        self.decreasing_slip_rate = decreasing_slip_rate

        
        self._init()


    def _init(self):
        self._load_nlin_initial_values()
        self._init_jacobian_vecs()
        self._init_decreasing_slip_rate_matrix()


    def _load_nlin_initial_values(self):
        self.nlin_par_initial_values = []
        for name in self.nlin_par_names:
            self.nlin_par_initial_values.append(self.G0[name])

        self.num_nlin_pars = len(self.nlin_par_initial_values)
        for name, val in self.iterate_nlin_par_name_val():
            setattr(self, name,val)
        
    def iterate_nlin_par_name_val(self):
        for name, val in zip(self.nlin_par_names, self.nlin_par_initial_values):
            yield name, val

    def _init_jacobian_vecs(self):
        dGs = []
        for G, par_name in zip(self.Gs, self.nlin_par_names):
            dGs.append(DifferentialG(ed1 = self.G0, ed2 = G, wrt = par_name))

        jacobian_vecs = []
        for dG in dGs:
            jacobian_vecs.append(JacobianVec(dG, self.slip0))

        self.jacobian_vecs = jacobian_vecs

    def _init_decreasing_slip_rate_matrix(self):
        if self.decreasing_slip_rate:
            mat1 = time_derivative_matrix(self.epochs)
            mat2 = inflate_time_derivative_matrix_by_num_subflts(mat1, self.num_subflts)
            self.GG = col_zeros_padding(mat2, self.num_nlin_pars)

        else:
            self.GG = None
    
    def set_data_B(self):
        print('Set data B ...')
        B = self.basis()
        self.B = eye_padding(B, self.num_nlin_pars)

    def set_data_L(self):
        print('Set data L ...')
        L = self.regularization()
        self.L = col_zeros_padding(L, self.num_nlin_pars)
        
        
    def set_data_G(self):
        super().set_data_G()
        jacobian = Jacobian()
        jacobian.G = self.G0
        jacobian.jacobian_vecs = self.jacobian_vecs
        jacobian.epochs = self.epochs
        self.G = jacobian()

    def set_data_d(self):
        super().set_data_d()
        d_ = D_()
        d_.jacobian_vecs = self.jacobian_vecs
        d_.nlin_par_values = self.nlin_par_initial_values
        d_.epochs = self.epochs

        d_.d = self.d
        self.d = d_()
        
        self.disp_obs = d_.disp_obs

    def set_data_sd(self):
        super().set_data_sd()
        self.sd = self.sd.stack(self.epochs)
        
    def predict(self):
        Bm = self.Bm
        Jac = self.G
        num_nlin_pars = self.num_nlin_pars

        npars0 = np.asarray(self.nlin_par_initial_values).reshape([-1,1])

        G = Jac[:,:-num_nlin_pars]

        Jac_ = Jac[:,-num_nlin_pars:]
        
        slip = Bm[:-num_nlin_pars,:]

        npars = Bm[-num_nlin_pars:,:]

        d = np.dot(G,slip)

        delta_nlin_pars = npars - npars0
        delta_d = np.dot(Jac_, delta_nlin_pars)

        d = d + delta_d

        self.d_pred = d


    def _compute_rms_inland_at_each_epoch(self): # TODO - How to handle misfits? Do I need this here?
        rms = []
        for nth, epoch in enumerate(self.epochs):
            ch = choose_inland_GPS_cmpts_at_nth_epochs(
                nth_epochs = nth,
                num_epochs = len(self.epochs)
                )
            rms.append(self.get_residual_rms(subset = ch))
        return np.asarray(rms,float)

    def get_residual_rms_at_inlands_sites(self):
        ch_inland = choose_inland_GPS_cmpts_for_all_epochs(
            self.sites,
            num_epochs = len(self.epochs))
        
        return self.get_residual_rms(ch_inland)

    def get_residual_norm(self, subset=None):
        '''
return: ||G B m - d||
'''
        diff = (self.d_pred - self.disp_obs)
        if subset is not None:
            assert len(subset)==len(diff), 'subset length is smaller than diff'
            diff = diff[subset]
        return np.linalg.norm(diff)

    def get_residual_norm_weighted(self):
        '''
return: ||W (G B m - d)||
'''
        diff = (self.d_pred - self.disp_obs)
        res_w = self.W.dot(diff)
        nres_w = np.linalg.norm(res_w)
        return nres_w
