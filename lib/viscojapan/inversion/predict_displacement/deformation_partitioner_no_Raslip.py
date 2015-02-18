import h5py

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
        super().__init__(
            file_G0 = file_G0,
            epochs = epochs,
            slip = slip,
            files_Gs = files_Gs,
            nlin_pars = nlin_pars,
            nlin_par_names = nlin_par_names,
            file_slip0 = file_slip0,
            sites_for_prediction = sites_for_prediction
             )

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
