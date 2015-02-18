import numpy as np
import h5py

from ..epoch_file_reader_for_inversion import EpochGNoRaslip, DifferentialGNoRaslip, EpochSlip

from .deformation_partitioner import DeformPartitioner

__all__ =['DeformPartitionerNoRaslip']
__author__ = 'zy'

class DeformPartitionerNoRaslip(DeformPartitioner):
    def __init__(self,
                 file_G0,
                 epochs,
                 slip,
                 files_Gs = None,
                 nlin_pars = None,
                 nlin_par_names = None,
                 file_slip0 = None,
                 sites_for_prediction = None
                 ):
        self.epochs = epochs
        self.num_epochs = len(self.epochs)

        self.G0 = EpochGNoRaslip(file_G0, mask_sites=sites_for_prediction)
        if sites_for_prediction is None:
            sites_for_prediction = self.G0.get_sites()

        self.sites_for_prediction = sites_for_prediction

        self.Gs = [EpochGNoRaslip(f, mask_sites=sites_for_prediction) for f in files_Gs]

        self.slip = slip

        self.nlin_par_vals = nlin_pars
        self.nlin_par_names = nlin_par_names


        self.slip0 = EpochSlip(file_slip0).respace(self.epochs)

        if files_Gs is not None:
            self._get_delta_nlin_pars()

    def _nlin_correction_E_cumu_slip(self, nth_epoch):
        epoch = self.epochs[nth_epoch]
        slip0 = self.slip0.get_cumu_slip_at_epoch(epoch).reshape([-1,1])
        dGs = []
        for Gi, par in zip(self.Gs, self.nlin_par_names):
            diffG = DifferentialGNoRaslip(ed1=self.G0, ed2=Gi, wrt=par)
            dGs.append(diffG[0])

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr

    def _nlin_correction_R_nth_epoch(self, from_nth_epoch, to_epoch):
        from_epoch = int(self.epochs[from_nth_epoch])

        slip0 = self.slip0.get_incr_slip_at_nth_epoch(from_nth_epoch).reshape([-1,1])

        del_epoch = int(to_epoch - from_epoch)

        dGs = []
        for Gi, par in zip(self.Gs, self.nlin_par_names):
            diffG = DifferentialGNoRaslip(ed1=self.G0, ed2=Gi, wrt=par)
            dG0 = diffG[0]
            dG = diffG[del_epoch]
            dGs.append(dG-dG0)

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr

    def R_aslip(self, epoch):
        raise NotImplementedError("There is no Raslip")

    def R_aslip_at_nth_epoch(self, nth):
        raise NotImplementedError("There is no Raslip")


    def R_aslip_to_disp_obj(self):
        raise NotImplementedError("There is no Raslip")

    # save to a file
    def save(self,fn):
        with h5py.File(fn,'w') as fid:
            print('Ecumu ...')
            disp3d_Ecumu = self.E_cumu_slip_to_disp_obj().get_cumu_disp_3d()
            fid['Ecumu'] = disp3d_Ecumu

            print('Rco ...')
            disp3d_Rco = self.R_co_to_disp_obj().get_cumu_disp_3d()
            fid['Rco'] = disp3d_Rco

            fid['d_added'] = disp3d_Ecumu + disp3d_Rco

            print('epochs ...')
            fid['epochs'] = self.epochs

            print('sites ...')
            fid['sites_for_prediction'] = [site.encode() for site in self.sites_for_prediction]
