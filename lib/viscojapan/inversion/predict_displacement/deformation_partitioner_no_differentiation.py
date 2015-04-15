import numpy as np
import h5py


from ..epoch_file_reader_for_inversion import EpochG, DifferentialG, EpochSlip
from ...sites import Site
from ...epoch_3d_array import Displacement

__all__ =['DeformPartitionerNoDifferentiation']
__author__ = 'zy'

class DeformPartitionerNoDifferentiation(object):
    def __init__(self,
                 file_G0,
                 epochs,
                 slip,
                 sites_for_prediction = None
                 ):

        self.epochs = epochs
        self.num_epochs = len(self.epochs)

        self.G0 = EpochG(file_G0, mask_sites=sites_for_prediction)
        if sites_for_prediction is None:
            sites_for_prediction = self.G0.get_sites()

        self.sites_for_prediction = sites_for_prediction

        self.slip = slip

    def E_cumu_slip(self, nth_epoch):
        cumuslip = self.slip.get_cumu_slip_at_nth_epoch(nth_epoch).reshape([-1,1])
        G0 = self.G0[0]
        disp = np.dot(G0, cumuslip)

        return disp

    def E_co(self):
        return self.E_cumu_slip(0)

    def E_aslip(self, nth_epoch):
        return self.E_cumu_slip(nth_epoch) - self.E_co()

    def R_nth_epoch(self, from_nth_epoch, to_epoch):
        epochs = self.epochs
        from_epoch = epochs[from_nth_epoch]

        del_epoch = to_epoch - from_epoch
        del_epoch = int(del_epoch)

        if del_epoch <= 0:
            return np.zeros([self.G0[0].shape[0],1])

        G = self.G0[del_epoch] - self.G0[0]
        s = self.slip.get_incr_slip_at_nth_epoch(from_nth_epoch).reshape([-1,1])
        disp = np.dot(G, s)

        return disp

    def R_co(self, epoch):
        return self.R_nth_epoch(0, epoch)

    def R_co_at_nth_epoch(self, nth):
        return self.R_co(self.epochs[nth])

    def R_aslip(self, epoch):
        num_epochs = self.num_epochs
        disp = None
        for nth in range(num_epochs):
            if nth == 0:
                continue
            if disp is None:
                disp = self.R_nth_epoch(nth, epoch)
            else:
                arr = self.R_nth_epoch(nth, epoch)
                disp += arr
        return disp

    def R_aslip_at_nth_epoch(self, nth):
        return self.R_aslip(self.epochs[nth])

    # output to displacement object
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

        sites = [Site(s) for s in self.G0.get_mask_sites()]
        disp = Displacement(cumu_disp_3d=res,
             epochs=self.epochs,
             sites = sites
        )

        return disp

    # save to a file
    def save(self,fn):
        with h5py.File(fn,'w') as fid:
            print('Ecumu ...')
            disp3d_Ecumu = self.E_cumu_slip_to_disp_obj().get_cumu_disp_3d()
            fid['Ecumu'] = disp3d_Ecumu

            print('Rco ...')
            disp3d_Rco = self.R_co_to_disp_obj().get_cumu_disp_3d()
            fid['Rco'] = disp3d_Rco

            print('Raslip ...')
            disp3d_Raslip = self.R_aslip_to_disp_obj().get_cumu_disp_3d()
            fid['Raslip'] = disp3d_Raslip

            fid['d_added'] = disp3d_Ecumu + disp3d_Rco + disp3d_Raslip

            print('epochs ...')
            fid['epochs'] = self.epochs

            print('sites ...')
            fid['sites_for_prediction'] = [site.encode() for site in self.sites_for_prediction]

