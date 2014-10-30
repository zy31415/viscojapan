import unittest
from os.path import join

import numpy as np

from viscojapan.pollitz import PollitzOutputsToEpochalData
from viscojapan.sites import Sites
from viscojapan.test_utils import MyTestCase

class Test_PollitzOutputsToEpochalData(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.clean_outs_dir()

    def test(self):
        visM = 1E19
        visK = 5E17
        rake = 90
        sites =  Sites.init_from_txt(join(self.share_dir, 'sites'))
        model = PollitzOutputsToEpochalData(                
            epochs = [0, 60],
            G_file = join(self.outs_dir, 'G.h5'),
            num_subflts = 10,
            pollitz_outputs_dir = join(self.share_dir, 'pollitz_outs'),
            sites = sites,
            extra_info ={
            'He':50,
            'visM':visM,
            'log10(visM)':np.log10(visM),
            'visK':visK,
            'log10(visK)':np.log10(visK),
            'rake':rake
            },
            extra_info_attrs ={
            'He':{'unit':'km'},
            'visM':{'unit':'Pa.s'},
            'visK':{'unit':'Pa.s'},
            }
            )
        model()
            
if __name__ == '__main__':
    unittest.main()
