from .deformation_partitioner import DeformPartitioner
from ..result_file import ResultFileReader

__author__ = 'zy'
__all__ = ['DeformPartitionerForResultFile']

class DeformPartitionerForResultFile(DeformPartitioner):
    def __init__(self,
                 file_G0,
                 result_file,
                 fault_file,
                 files_Gs = None,
                 file_incr_slip0 = None,
                 sites_for_prediction = None
                 ):

        result_file_reader = ResultFileReader(result_file)
        self.result_file_reader = result_file_reader

        super().__init__(file_G0 = file_G0,
                         epochs = result_file_reader.epochs,
                         slip = result_file_reader.get_slip(fault_file=fault_file),
                         files_Gs = files_Gs,
                         nlin_pars = result_file_reader.nlin_par_solved_values,
                         nlin_par_names = result_file_reader.nlin_par_names,
                         file_incr_slip0 = file_incr_slip0, # TODO change file_incr_slip0 to slip object to allow more flexibility.
                         sites_for_prediction = sites_for_prediction
                         )
