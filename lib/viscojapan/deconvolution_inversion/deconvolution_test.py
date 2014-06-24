from os.path import join, exists
from os import makedirs

from .deconvolution import Deconvolution
from ..inversion_test import gen_error_for_sites

class DeconvolutionTestFromFakeObs(Deconvolution):
    def __init__(self):
        super().__init__()
        self.num_err = None
        self.east_st = None
        self.north_st = None
        self.up_st = None

    def _get_d(self):
        d = super()._get_d()        
        err = gen_error_for_sites(self.num_err,
                                  self.east_st, self.north_st, self.up_st)
        d += err
        return d

    
                    
        
