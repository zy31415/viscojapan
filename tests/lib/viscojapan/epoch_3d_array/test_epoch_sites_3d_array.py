from os.path import join
import unittest

import numpy as np
import h5py

import viscojapan as vj

class Test_EpochSites3DArray(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_load_and_save(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'
        with h5py.File(fn,'r') as fid:
            arr = vj.epoch_3d_array.EpochSites3DArray.load(fid,
                                                           memory_mode=False)

            arr.save(join(self.outs_dir, 'G.h5'))

    def test_get_array_3d(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/cumu_post_with_seafloor.h5'
        with h5py.File(fn,'r') as fid:
            arr = vj.epoch_3d_array.EpochSites3DArray.load(
                fid,
                mask_sites = ['J550'],
                memory_mode=False)

            out = arr.get_array_3d()

            arr.set_mask_sites(['J550','J551'])

            out = arr.get_array_3d()

            arr.save(join(self.outs_dir, 'obs.h5'))

            print(out.shape)



if __name__ == '__main__':
    unittest.main()




