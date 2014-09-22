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
from ..utils import _assert_column_vector
from .occam_deconvolution import OccamDeconvolutionSeparateCoPost

__all__=['OccamDeconvolutionSeparateCoPost']

def eye_padding(mat, n):
    pad = sparse.eye(n)
    return sparse.block_diag((mat, pad))

def col_zeros_padding(mat, n):
    sh = mat.shape[0]
    pad = sparse.csr_matrix((sh,n))
    return sparse.hstack((mat, pad))
    

class OccamDeconvolutionSeparateCoPost(OccamDeconvolution):
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
        super().__init__(file_G0, files_Gs, nlin_par_names,
                         file_d, file_sd, filter_sites_file, epochs,
                         regularization, basis, file_incr_slip0,)

        ep = vj.EpochalIncrSlip(self.file_incr_sip0)
        self.num_subflts = len(ep[0].flatten())
    
    def set_data_B(self):
        super().set_data_B()
        self.B = self.B[:, self.num_subflts:]

    def set_data_L(self):
        super().set_data_L()
        self.L = self.B[:, self.num_subflts:]
        
    def set_data_G(self):
        super().set_data_G()
        self.G[self.num_subflts:, self.num_subflts:]

    def set_data_d(self):
        super().set_data_d()
        self.d = self.d[self.num_subflts:,:]
        #self.disp_obs = d_.disp_obs

    def set_data_sd(self):
        super().set_data_sd()
        self.sd = self.sdself.num_subflts:,:]
        
