import unittest
import os
from os.path import join

import viscojapan as vj


class Test_EpochalFileReader(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test1(self):
        reader = vj.inv.ep.EpochFileReader(join(self.share_dir,'G0_He50km_VisM6.3E18_Rake83.h5'))

        for day in range(0,100):
            out = reader.get_data_at_epoch(day)


if __name__== '__main__':
    unittest.main()
