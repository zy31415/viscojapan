import numpy as np

import viscojapan as vj
from .occam_deconvolution import OccamDeconvolution

__all__=['OccamDeconvolutionSeparateCoPost']

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
                         regularization, basis, file_incr_slip0)

        assert self.epochs[0] == 0, 'The first epoch must be zero.'
        self.num_epochs = len(self.epochs) - 1

        ep = vj.EpochalIncrSlip(file_incr_slip0)
        self.num_subflts = len(ep[0].flatten())

        ep = vj.EpochalDisplacement(file_sd, filter_sites_file)
        self.num_obs = len(ep[0].flatten())

        self._compute_disp_caused_by_coseismic_slip()
        
    def set_data_G(self):
        super().set_data_G()
        self.G = self.G[self.num_obs:, self.num_subflts:]

    def _compute_disp_caused_by_coseismic_slip(self):
        self.co_slip = vj.EpochalIncrSlip(self.file_incr_slip0)[0]
        coseismic_disp = []        
        ep = vj.EpochalG(self.file_G0, self.filter_sites_file)        
        for nth, epoch in enumerate(self.epochs):
            G = ep[epoch]
            d_co = np.dot(G, self.co_slip)
            coseismic_disp.append(d_co)
        self.coseismic_disp = np.vstack(coseismic_disp)

    def set_data_d(self):
        super().set_data_d()
        self.d -= self.coseismic_disp 
        self.d = self.d[self.num_obs:,:]
        self.disp_obs = self.disp_obs[self.num_obs:,:]

    def set_data_sd(self):
        super().set_data_sd()
        self.sd = self.sd[self.num_obs:,:]

    def predict(self):
        super().predict()
        self.d_pred += self.coseismic_disp[self.num_obs:,:]
        self.least_square.d_pred = self.d_pred
        
