import numpy as np

from .deformation_partitioner import DeformPartitioner
from ..result_file import ResultFileReader

__all__ = ['DispPred']

class DispPred(DeformPartitioner):
    def __init__(self,
                 file_G0,
                 result_file,
                 fault_file,
                 files_Gs = None,
                 nlin_par_names = None,
                 file_incr_slip0 = None,
                 ):

        self.result_file = result_file
        res_reader = ResultFileReader(self.result_file)
        self.fault_file = fault_file

        super().__init__(file_G0 = file_G0,
                         epochs = res_reader.epochs,
                         slip = res_reader.get_slip(self.fault_file),
                         files_Gs = files_Gs,
                         nlin_pars = res_reader.nlin_pars,
                         nlin_par_names = nlin_par_names,
                         file_incr_slip0 = file_incr_slip0,
                         )