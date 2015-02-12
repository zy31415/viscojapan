import unittest
import os
from os.path import join

import viscojapan as vj


class Test_EpochSlip(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test1(self):
        file = join(self.share_dir,'slip0.h5')
        slip = vj.inv.ep.EpochSlip(file)

        stacked = slip.stack([0,10])
        print(stacked)



if __name__== '__main__':
    unittest.main()
