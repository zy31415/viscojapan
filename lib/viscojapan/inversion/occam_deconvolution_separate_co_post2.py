import numpy as np

import viscojapan as vj
from .occam_deconvolution import OccamDeconvolution

__all__=['OccamDeconvolutionSeparateCoPost2']

class OccamDeconvolutionSeparateCoPost2(OccamDeconvolution):
    ''' Connet relative objects to work together to do inversion.
'''
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
                 file_co_slip,
                 ):
        super().__init__(file_G0, files_Gs, nlin_par_names,
                         file_d, file_sd, sites, epochs,
                         regularization, basis, file_slip0)

        assert self.epochs[0]>0
        self.num_epochs = len(self.epochs)

        ep = vj.EpochalIncrSlip(file_slip0)
        self.num_subflts = len(ep[0].flatten())

        ep = vj.EpochalDisplacement(file_sd, sites)
        self.num_obs = len(ep[0].flatten())

        self.file_co_slip = file_co_slip
        self._compute_disp_caused_by_coseismic_slip()


    def _compute_disp_caused_by_coseismic_slip(self):
        self.co_slip = vj.EpochalIncrSlip(self.file_co_slip)[0]
        coseismic_disp = []        
        ep = vj.EpochalG(self.file_G0, self.sites)
        G0 = ep[0]
        for nth, epoch in enumerate(self.epochs):
            G = ep[epoch]
            d_co = np.dot(G-G0, self.co_slip)
            coseismic_disp.append(d_co)
        self.coseismic_disp = np.vstack(coseismic_disp)

    def set_data_d(self):
        super().set_data_d()
        self.d -= self.coseismic_disp 
        
    def predict(self):
        super().predict()
        self.d_pred += self.coseismic_disp
        self.least_square.d_pred = self.d_pred
        
