from os.path import join
import unittest

import numpy as np
import h5py

import viscojapan as vj
from viscojapan.epoch_3d_array.epoch_3d_array import _Epoch3DArray

class Test__Epoch3DArray(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_ndarray_as_array_3d(self):
        arr3d = np.ones([10,20,3])
        epochs = range(0,10)
        arr = _Epoch3DArray(array_3d = arr3d,
                            epochs = epochs)

        arr.get_array_3d()

        arr.save(join(self.outs_dir,'saved.h5'))

    def test_hdf5_as_array_3d(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'
        fid = h5py.File(fn)
        array_3d = fid['data3d']
        epochs = range(0,28)
        arr = _Epoch3DArray(array_3d = array_3d,
                            epochs = epochs)

        print(type(arr.get_array_3d()))
        print(arr.get_epochs())

        arr.save(join(self.outs_dir,'G.h5'))

    def test_load(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'
        with h5py.File(fn,'r') as fid:
            arr = _Epoch3DArray.load(fid, False)


class Test_Epoch3DArray(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'
        with h5py.File(fn,'r') as fid:
            arr = vj.epoch_3d_array.Epoch3DArray.load(fid, False)

            vel3d = arr.get_velocity_3d()

            data = arr.get_data_at_nth_epoch(0)

            data = arr.get_data_at_epoch_no_interpolation(60)

            data = arr.get_data_at_epoch(1620)

            #print(data)






if __name__ == '__main__':
    unittest.main()



