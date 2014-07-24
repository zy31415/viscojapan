from numpy import asarray, dot, zeros, vstack
import scipy.sparse as sparse
import h5py

from ..epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD, DiffED, EpochalIncrSlip
from .formulate_occam import JacobianVec, Jacobian, D_
from .inversion import Inversion
from ..utils import _assert_column_vector, delete_if_exists

def eye_padding(mat, n):
    pad = sparse.eye(n)
    return sparse.block_diag((mat, pad))

def col_zeros_padding(mat, n):
    sh = mat.shape[0]
    pad = sparse.csr_matrix((sh,n))
    return sparse.hstack((mat, pad))
    

class OccamDeconvolution2(Inversion):
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self,
                 file_G0,
                 files_Gs,
                 nlin_par_names,                 
                 file_d,
                 file_sd,
                 file_incr_slip0,
                 filter_sites_file,
                 epochs,                 
                 regularization,
                 basis,
                 ):
        
        self.file_G0 = file_G0
        self.files_Gs = files_Gs
        
        self.nlin_par_names = nlin_par_names
        
        self.file_d = file_d
        self.file_sd = file_sd
        
        self.file_incr_slip0 = file_incr_slip0
        self.filter_sites_file = filter_sites_file
        self.epochs = epochs

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
        g_obj = EpochalG(self.file_G0, self.filter_sites_file)
        G  = g_obj.conv_stack(self.epochs)

        incr_slip_obj = EpochalIncrSlip(self.file_incr_slip0)
        incr_slip = incr_slip_obj.vstack()

        disp_obj = EpochalDisplacement(self.file_d, self.filter_sites_file)
        disp = disp_obj.vstack(self.epochs)
        
        self.d = disp - dot(G, incr_slip)

    def set_data_sd(self):
        super().set_data_sd()
        sig = EpochalDisplacementSD(self.file_sd, self.filter_sites_file)
        sig_stacked = sig.vstack(self.epochs)
        self.sd = sig_stacked
        _assert_column_vector(self.sd)

    def set_data_Bm0(self):
        print("Set data Bm0.")
        incr_slip_obj = EpochalIncrSlip(self.file_incr_slip0)
        incr_slip = incr_slip_obj.vstack()
        pad = zeros([self.num_nlin_pars,1])
        Bm0 = vstack([incr_slip, pad])
        self.Bm0 = Bm0
        print(self.Bm0.shape)

    def save(self, fn, overwrite = False):
        print('Saving ...')
        if overwrite:
            delete_if_exists(fn)
        ls = self.least_square
        with h5py.File(fn) as fid:
            fid['m'] = ls.m
            fid['Bm'] = ls.Bm
            fid['d_pred'] = self.d_pred
            fid['residual_norm'] = ls.get_residual_norm()
            fid['residual_norm_weighted'] = ls.get_residual_norm_weighted()

            for par, name in zip(self.regularization.args,
                                 self.regularization.arg_names):
                fid['regularization/%s/coef'%name] = par
                
            for nsol, name in zip(self.regularization.components_solution_norms(ls.Bm),
                                  self.regularization.arg_names):
                fid['regularization/%s/norm'%name] = nsol
