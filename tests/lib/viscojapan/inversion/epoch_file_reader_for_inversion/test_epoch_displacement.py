import unittest
from os.path import join

import viscojapan as vj


class Test_EpochDisplacement(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test1(self):
        mask_sites = ['J550', 'J456']
        file = '/home/zy/workspace/viscojapan/tests/share/cumu_post_with_seafloor.h5'
        G = vj.inv.ep.EpochDisplacement(file,
                             mask_sites= mask_sites)

        out = G.get_data_at_epoch(0)

        stacked = G.stack([0,60])
        print(stacked)

class Test_EpochDisplacementSD(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        mask_sites = ['J550', 'J456']
        file = join(self.share_dir,'sd_uniform.h5')
        G = vj.inv.ep.EpochDisplacementSD(file,
                                          mask_sites= mask_sites)

        out = G.get_data_at_epoch(0)

        stacked = G.stack([0,60])
        print(stacked)


if __name__== '__main__':
    unittest.main()
