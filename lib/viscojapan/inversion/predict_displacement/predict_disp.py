import numpy as np

from .deformation_partitioner_to_disp_obj import DeformPartitioner2Disp
from ..result_file import ResultFileReader

__all__ = ['DispPred']

class DispPred(DeformPartitioner2Disp):
    def __init__(self,
                 file_G0,
                 result_file,
                 fault_file,
                 files_Gs = None,
                 nlin_par_names = None,
                 file_incr_slip0 = None,
                 ):

        self.result_file = result_file
        self.result_file_reader = ResultFileReader(self.result_file)
        self.fault_file = fault_file

        self.sites_in_inversion = self.result_file_reader.sites

        super().__init__(file_G0 = file_G0,
                         epochs = self.result_file_reader.epochs,
                         slip = self.result_file_reader.get_slip(self.fault_file),
                         files_Gs = files_Gs,
                         nlin_pars = self.result_file_reader.nlin_pars,
                         nlin_par_names = nlin_par_names,
                         file_incr_slip0 = file_incr_slip0,
                         )

    def check_partition_result(self):
        pred = self.result_file_reader.get_pred_disp().cumu3d

        Ecumu = self.E_cumu_slip_to_disp_obj().cumu3d
        Rco = self.R_co_to_disp_obj().cumu3d
        Raslip = self.R_aslip_to_disp_obj().cumu3d

        np.testing.assert_array_almost_equal(pred, Ecumu+Rco+Raslip)

        print('Pass checking! Prediction equals components added!')
