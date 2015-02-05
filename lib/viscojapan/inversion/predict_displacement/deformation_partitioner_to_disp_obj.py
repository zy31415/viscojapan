import numpy as np
import h5py

from .deformation_partitioner import DeformPartitioner
from ...displacement import Disp
from ...sites import Site

__author__ = 'zy'
__all__ = ['DeformPartitioner2Disp']

class DeformPartitioner2Disp(DeformPartitioner):
    def __init__(self,
                 file_G0,
                 epochs,
                 slip,
                 files_Gs = None,
                 nlin_pars = None,
                 nlin_par_names = None,
                 file_incr_slip0 = None,
                 ):
        super().__init__(
            file_G0 = file_G0,
            epochs = epochs,
            slip = slip,
            files_Gs = files_Gs,
            nlin_pars = nlin_pars,
            nlin_par_names = nlin_par_names,
            file_incr_slip0 = file_incr_slip0,
        )

    def E_cumu_slip_to_disp_obj(self):
        return self._form_disp_obj(self.E_cumu_slip)

    def E_aslip_to_disp_obj(self):
        return self._form_disp_obj(self.R_aslip)

    def R_co_to_disp_obj(self):
        return self._form_disp_obj(self.R_co_at_nth_epoch)

    def R_aslip_to_disp_obj(self):
        return self._form_disp_obj(self.R_aslip_at_nth_epoch)

    def _form_disp_obj(self, func):
        res = []
        for nth, epoch in enumerate(self.epochs):
            res.append(func(nth).reshape([-1, 3]))

        res = np.asarray(res)

        sites = [Site(s) for s in self.file_G0_reader.filter_sites]
        disp = Disp(cumu_disp3d=res,
             epochs=self.epochs,
             sites = sites
        )

        return disp

    def save(self,fn):
        with h5py.File(fn,'w') as fid:
            disp = self.E_cumu_slip_to_disp_obj()
            fid['Ecumu'] = disp.cumu3d
            fid['Rco'] = self.R_co_to_disp_obj().cumu3d
            fid['Raslip'] = self.R_aslip_to_disp_obj().cumu3d
            fid['epochs'] = self.epochs
            fid['sites'] = [site.id.encode() for site in disp.sites]
