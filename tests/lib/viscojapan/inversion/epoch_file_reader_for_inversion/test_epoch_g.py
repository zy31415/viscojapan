import unittest
import os
from os.path import join

import viscojapan as vj


class Test_EpochG(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test1(self):
        file_G = join(self.share_dir,'G0_He50km_VisM6.3E18_Rake83.h5')
        G = vj.inv.ep.EpochG(file_G,
                             mask_sites= ['J550'])

        out = G.get_data_at_epoch(0)

        stacked = G.stack([0,60,120])

class Test_DifferentialG(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test1(self):
        mask_sites = ['J550', 'J456']
        file_G1 = join(self.share_dir,'G0_He50km_VisM6.3E18_Rake83.h5')
        G1 = vj.inv.ep.EpochG(file_G1,
                             mask_sites= mask_sites)

        file_G2 = join(self.share_dir,'G1_He50km_VisM1.0E19_Rake83.h5')
        G2 = vj.inv.ep.EpochG(file_G2,
                             mask_sites= mask_sites)

        diffG = vj.inv.ep.DifferentialG(ed1=G1, ed2=G2, wrt='log10(visM)')

        stacked = diffG.stack([0,60,120])


if __name__== '__main__':
    unittest.main()
