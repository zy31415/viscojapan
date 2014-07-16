from numpy import asarray, loadtxt, dot

from viscojapan.epochal_data import EpochalG
from ..inversion import Inversion
from .inversion_test_utils import  gen_error_for_sites

class StaticInversionTest(Inversion):
    def __init__(self,
                 file_G,
                 file_sites_filter,
                 slip_true,
                 sd_horizontal,
                 sd_up,
                 regularization,
                 basis,
                 ):
        
        self.file_G = file_G
        self.file_sites_filter = file_sites_filter
        self.slip_true = slip_true
        
        self.sd_horizontal = sd_horizontal
        self.sd_up = sd_up
        super().__init__(
            regularization = regularization,
            basis = basis,)

    def get_num_sites(self):
        sites = loadtxt(self.file_sites_filter,'4a')
        num_sites = len(sites)
        return num_sites

    def set_data_sd(self):
        num_sites = self.get_num_sites()
        self.sd = asarray([[self.sd_horizontal, self.sd_horizontal, self.sd_up]*num_sites]).\
                   reshape([-1, 1])

    def set_data_G(self):
        G_ep = EpochalG(self.file_G, self.file_sites_filter)
        self.G = G_ep(0)

    def set_data_d(self):
        m_true = self.slip_true
        B = self.basis()
        d_true = dot(self.G,B.dot(m_true))
        
        self.east_st = self.north_st = self.sd_horizontal
        self.up_st = self.sd_up

        num_sites = self.get_num_sites()
        error = gen_error_for_sites(num_sites,
                    self.east_st, self.north_st, self.up_st)
        self.d = d_true + error
        



        

