from os.path import exists

import h5py
from numpy import loadtxt, asarray

from .efr_sites_filtered import EFRSitesFiltered

class GFilteredReader(EFRSitesFiltered):
    ''' Fliter a G matrix according a new station list.
'''
    def __init__(self, epoch_reader, sites_file):
        super().__init__(epoch_reader, sites_file)        
        
