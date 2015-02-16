from os.path import join
import unittest

import numpy as np
import h5py

import viscojapan as vj

class Test_Slip(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/slip0.h5'

        with h5py.File(fn,'r') as fid:
            arr = vj.epoch_3d_array.Slip.load(fid)

            data = arr.get_cumu_slip_3d()

            data = arr.get_coseismic_slip()

            data = arr.get_incr_slip_3d()

            data = arr.get_cumu_slip_at_nth_epoch(3)

            data = arr.get_cumu_slip_at_epoch(1000)

            data = arr.get_incr_slip_at_nth_epoch(5)

            data = arr.get_incr_slip_at_epoch(436)

            data = arr.get_afterslip_at_nth_epoch(10)

            data = arr.get_slip_rate_at_nth_epoch(0)
            data = arr.get_slip_rate_at_nth_epoch(1)

            data = arr.get_incr_slip_at_subfault(2,10)

            data = arr.get_slip_rate_at_subfault(2, 10)
            #print(data)

            #print(arr.get_array_3d())


    def test_respace(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/slip0.h5'

        with h5py.File(fn,'r') as fid:
            arr = vj.epoch_3d_array.Slip.load(fid)

            arr1 = arr.respace([0, 100, 200, 300])








if __name__ == '__main__':
    unittest.main()




