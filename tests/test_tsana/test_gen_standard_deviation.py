import unittest
from os.path import join

from pylab import plt
import numpy as np

from viscojapan.tsana.gen_standard_deviation import \
     GenUniformOnshoreSDWithInfiniteSeafloorSD, \
     copy_and_revise_sd_file
     
from viscojapan.test_utils import MyTestCase

class Test_gen_standard_deviation(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.sites = np.loadtxt(join(self.share_dir, 'sites_with_seafloor'),
                                '4a',usecols=(0,))
        self.clean_outs_dir()

        
    def test_GenUniformOnshoreSDWithInfiniteSeafloorSD(self):        
        gen = GenUniformOnshoreSDWithInfiniteSeafloorSD(
            sites = self.sites,
            days = range(0,30),
            sd_co_hor = 1,
            sd_co_ver = 5,
            sd_post_hor = 2,
            sd_post_ver = 10, 
            )
        gen.save(join(self.outs_dir, '~sd.h5'))

    def test_copy_and_revise_sd_file(self):
        self.clean_outs_dir()
        self.test_GenUniformOnshoreSDWithInfiniteSeafloorSD()
        copy_and_revise_sd_file(
            file_sd_original = join(self.outs_dir, '~sd.h5'),
            file_seafloor_sd = join(self.share_dir, 'seafloor_sd'),
            file_sd_out = join(self.outs_dir, '~sd_seafloor.h5'),
            sd = None)
        
if __name__ == '__main__':
    unittest.main()
