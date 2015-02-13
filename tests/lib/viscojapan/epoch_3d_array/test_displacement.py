from os.path import join
import unittest

import numpy as np
import h5py

import viscojapan as vj

class Test_Displacement(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_get_cumu_disp_3d_not_ordered(self):
        '''
        This test is slow.
        '''
        fn = '/home/zy/workspace/viscojapan/tests/share/cumu_post_with_seafloor.h5'
        with h5py.File(fn,'r') as fid:
            sites = vj.utils.as_string(fid['sites'])

            arr = vj.epoch_3d_array.Displacement.load(
                fid,
                mask_sites = sites[2:] + sites[:1],
                memory_mode=False)

            out = arr.get_cumu_disp_3d()

    def test_get_cumu_disp_3d_ordered(self):
        '''
        This test is fast.
        '''
        fn = '/home/zy/workspace/viscojapan/tests/share/cumu_post_with_seafloor.h5'
        with h5py.File(fn,'r') as fid:
            sites = vj.utils.as_string(fid['sites'])

            arr = vj.epoch_3d_array.Displacement.load(
                fid,
                mask_sites = sites,
                memory_mode=False)

            out = arr.get_cumu_disp_3d()

    def test(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/cumu_post_with_seafloor.h5'
        with h5py.File(fn,'r') as fid:

            arr = vj.epoch_3d_array.Displacement.load(
                fid,
                mask_sites = ['J550'],
                memory_mode=False)

            out = arr.get_post_disp_3d()
            out = arr.get_coseismic_disp()
            out = arr.get_cumu_at_nth_epoch(500)
            out = arr.cumu_ts('J550','u')
            out = arr.post_ts('J550','u')
            out = arr.vel_ts('J550','u')
            print(out)






if __name__ == '__main__':
    unittest.main()




