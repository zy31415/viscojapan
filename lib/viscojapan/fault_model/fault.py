from .fault_file_reader import FaultFileReader

__author__ = 'zy'
__all__ = ['Fault']

class Fault(FaultFileReader):
    def __init__(self, fault_file):
        super().__init__(fault_file=fault_file)
