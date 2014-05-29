'''
'''
from os.path import exists

import h5py
from numpy import asarray, loadtxt

from .ef_reader import EFReader

class GReader(EFReader):
    ''' This class is used for G files.
'''
    def __init__(self, epoch_file):
        super().__init__(epoch_file)
        
