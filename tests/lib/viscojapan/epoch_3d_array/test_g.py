from os.path import join
import unittest

import numpy as np
import h5py

import viscojapan as vj

class Test_G(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test_ordered_mask_sties(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'

        with h5py.File(fn,'r') as fid:
            sites = vj.utils.as_string(fid['sites'])
            arr = vj.epoch_3d_array.G.load(
                fid,
                mask_sites = sites,
                memory_mode=False)

            #print(arr.get_array_3d())

    def test_not_ordered_mask_sites(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'

        with h5py.File(fn,'r') as fid:
            sites = vj.utils.as_string(fid['sites'])
            arr = vj.epoch_3d_array.G.load(
                fid,
                mask_sites = sites[2:]+sites[0:2],
                memory_mode=False)

            print(arr.get_array_3d())







if __name__ == '__main__':
    unittest.main()




