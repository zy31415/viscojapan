import tempfile as tf

from numpy import asarray, dot
from numpy.linalg import norm
import numpy as np
import scipy.sparse as sparse
import h5py

import viscojapan as vj
from ..epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD, DiffED
from .formulate_occam import JacobianVec, Jacobian, D_
from .inversion import Inversion
from ..utils import assert_col_vec_and_get_nrow

__all__ = ['OccamDeconvolution']

def eye_padding(mat, n):
    pad = sparse.eye(n)
    return sparse.block_diag((mat, pad))

def col_zeros_padding(mat, n):
    sh = mat.shape[0]
    pad = sparse.csr_matrix((sh,n))
    return sparse.hstack((mat, pad))
    

class OccamDeconvolution(Inversion):
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self,
                 file_G0,
                 files_Gs,
                 nlin_par_names,                 
                 file_d,
                 file_sd,
                 filter_sites_file,
                 epochs,                 
                 regularization,
                 basis,
                 file_incr_slip0,
                 ):
        
        self.file_G0 = file_G0
        self.files_Gs = files_Gs
        
        self.nlin_par_names = nlin_par_names
        
        self.file_d = file_d
        self.file_sd = file_sd
        
        self.file_incr_slip0 = file_incr_slip0
        
        self.filter_sites_file = filter_sites_file
        self.epochs = epochs
        self.num_epochs = len(self.epochs)

        super().__init__(
            regularization,
            basis,)
        
        self._init()
        self._init_jacobian_vecs()

    def _load_nlin_initial_values(self):
        self.nlin_par_initial_values = []
        g = EpochalG(self.file_G0)
        for name in self.nlin_par_names:
            self.nlin_par_initial_values.append(float(g[name]))
        
    def iterate_nlin_par_name_val(self):
        for name, val in zip(self.nlin_par_names, self.nlin_par_initial_values):
            yield name, val        

    def _init(self):
        self._load_nlin_initial_values()
        self.num_nlin_pars = len(self.nlin_par_initial_values)
        for name, val in self.iterate_nlin_par_name_val():
            setattr(self, name,val)

    def _init_jacobian_vecs(self):
        self.G0 = EpochalG(self.file_G0, self.filter_sites_file)

        Gs = []
        for file_G in self.files_Gs:
            Gs.append(EpochalG(file_G, self.filter_sites_file))

        dGs = []
        for G, par_name in zip(Gs, self.nlin_par_names):
            dGs.append(
                DiffED(ed1 = self.G0, ed2 = G,
                       wrt = par_name))

        # repacing input initial incr slip.
        file_incr_slip0 = '~incr_slip0_respacing.h5'
        vj.delete_if_exists(file_incr_slip0)
        vj.EpochalIncrSlip(self.file_incr_slip0).respacing(
            self.epochs, file_incr_slip0)
        self.file_incr_slip0 = file_incr_slip0
        
        jacobian_vecs = []
        for dG in dGs:
            jacobian_vecs.append(JacobianVec(dG, self.file_incr_slip0))
        self.jacobian_vecs = jacobian_vecs
    
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

        obs = EpochalDisplacement(self.file_d, self.filter_sites_file)
        d_.d = obs        
        self.d = d_()
        self.disp_obs = d_.disp_obs

    def set_data_sd(self):
        super().set_data_sd()
        sig = EpochalDisplacementSD(self.file_sd, self.filter_sites_file)
        sig_stacked = sig.vstack(self.epochs)
        self.sd = sig_stacked
        assert_col_vec_and_get_nrow(self.sd)
        
        
    def predict(self):
        Bm = self.Bm
        Jac = self.G
        num_nlin_pars = self.num_nlin_pars

        npars0 = asarray(self.nlin_par_initial_values).reshape([-1,1])

        G = Jac[:,:-num_nlin_pars]

        Jac_ = Jac[:,-num_nlin_pars:]
        
        slip = Bm[:-num_nlin_pars,:]

        npars = Bm[-num_nlin_pars:,:]

        d = dot(G,slip)

        delta_nlin_pars = npars - npars0
        delta_d = dot(Jac_, delta_nlin_pars)

        d = d + delta_d

        self.d_pred = d

    def _choose_inland_observation_at_epoch(self, nth_epoch):
        sites = np.loadtxt(self.filter_sites_file,'4a,')
        ch1 = vj.choose_inland_GPS_for_cmpts(sites)
        ch2 = [False]*len(ch1)
        
        out = []        
        for nth in range(self.num_epochs):
            if nth == nth_epoch:
                out.append(ch1)
            else:
                out.append(ch2)
        out = np.asarray(out).flatten()
        return out
            
    def _compute_rms_inland_at_each_epoch(self):
        rms = []
        for nth in range(self.num_epochs):
            ch = self._choose_inland_observation_at_epoch(nth)
            rms.append(self.get_residual_rms(subset = ch))
        return np.asarray(rms,float)

    def get_residual_rms(self, subset=None):
        diff = (self.d_pred - self.disp_obs)
        if subset is not None:
            assert len(subset)==len(diff), 'subset length is smaller than diff'
            diff = diff[subset]
        return np.sqrt(np.mean(diff**2))

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
        nres_w = norm(res_w)
        return nres_w

    def _save_non_linear_par_correction(self, fid):
        Bm = self.Bm
        Jac = self.G
        num_nlin_pars = self.num_nlin_pars
        npars0 = asarray(self.nlin_par_initial_values)

        Jac_ = Jac[:,-num_nlin_pars:]
        npars = Bm[-num_nlin_pars:,:]
        
        delta_nlin_pars = npars.flatten() - npars0
        fid['nlin_correction'] = delta_nlin_pars*Jac_
        

    def save(self, fn, overwrite = False):
        super().save(fn, overwrite)
        sites = np.loadtxt(self.filter_sites_file,'4a,')
        ch_inland = vj.choose_inland_GPS_for_cmpts(
            sites, num_epochs= self.num_epochs)
        with h5py.File(fn) as fid:
            num_nlin_par = len(self.nlin_par_names)
            for nth, pn in enumerate(self.nlin_par_names):
                fid['nlin_pars/'+pn] = self.Bm[nth - num_nlin_par,0]
            fid['sites'] = sites
            fid['epochs'] = self.epochs
            fid['misfit/rms_inland'] = self.get_residual_rms(subset=ch_inland)
            fid['misfit/rms_inland_at_epoch'] = self._compute_rms_inland_at_each_epoch()
            self._save_non_linear_par_correction(fid)

            
