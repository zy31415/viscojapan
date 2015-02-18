import numpy as np

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
            file_G0=file_G0,
            epochs=epochs,
            slip=slip,
            files_Gs=files_Gs,
            nlin_pars=nlin_pars,
            nlin_par_names=nlin_par_names,
            file_slip0=file_slip0,
            sites_for_prediction=sites_for_prediction,
        )

    def R_nth_epoch(self, from_nth_epoch, to_epoch):
        if int(from_nth_epoch) == 0:
            return super().R_nth_epoch(0, to_epoch)
        return np.zeros([self.G0[0].shape[0], 1])
