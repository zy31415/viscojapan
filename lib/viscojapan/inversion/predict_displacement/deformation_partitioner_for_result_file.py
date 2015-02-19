from .deformation_partitioner import DeformPartitioner
from .deformation_partitioner_no_Raslip import DeformPartitionerNoRaslip

from ..result_file import ResultFileReader

__author__ = 'zy'
__all__ = ['DeformPartitionerForResultFile',
           'DeformPartitionerNoRaslipForResultFile']

class DeformPartitionerForResultFile(DeformPartitioner): # TODO: Replace this class with factory method.
    def __init__(self,
                 file_G0,
                 result_file,
                 files_Gs = None,
                 file_slip0 = None,
                 sites_for_prediction = None
                 ):

        result_file_reader = ResultFileReader(result_file)
        self.result_file_reader = result_file_reader

        super().__init__(file_G0 = file_G0,
                         epochs = result_file_reader.epochs,
                         slip = result_file_reader.get_slip(),
                         files_Gs = files_Gs,
                         nlin_pars = result_file_reader.nlin_par_solved_values,
                         nlin_par_names = result_file_reader.nlin_par_names,
                         file_slip0 = file_slip0,
                         sites_for_prediction = sites_for_prediction
                         )

class DeformPartitionerNoRaslipForResultFile(DeformPartitionerNoRaslip): # TODO: Replace this class with factory method.
    def __init__(self,
                 file_G0,
                 result_file,
                 files_Gs = None,
                 file_slip0 = None,
                 sites_for_prediction = None
                 ):

        result_file_reader = ResultFileReader(result_file)
        self.result_file_reader = result_file_reader

        super().__init__(file_G0 = file_G0,
                         epochs = result_file_reader.epochs,
                         slip = result_file_reader.get_slip(),
                         files_Gs = files_Gs,
                         nlin_pars = result_file_reader.nlin_par_solved_values,
                         nlin_par_names = result_file_reader.nlin_par_names,
                         file_slip0 = file_slip0,
                         sites_for_prediction = sites_for_prediction
                         )