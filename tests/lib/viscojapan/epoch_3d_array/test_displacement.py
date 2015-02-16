from os.path import join
import unittest

import numpy as np
import pylab as plt
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
            out = arr.get_cumu_at_epoch(101)
            out = arr.get_post_at_epoch(89)
            out = arr.get_post_hor_mag_at_epoch(333)

            print(out)

    def test_disp_interpolation(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        reader = vj.inv.ResultFileReader(fn)
        arr = reader.get_pred_disp()

        arr.set_mask_sites(['J550'])

        disp = []
        epochs = range(1200)
        for epoch in epochs:
            tp = arr.get_cumu_at_epoch(epoch)
            disp.append(tp[0])

        plt.plot(epochs, disp)

        disp = []
        epochs = arr.get_epochs()
        for epoch in epochs:
            tp = arr.get_cumu_at_epoch(epoch)
            disp.append(tp[0])

        plt.plot(epochs, disp,'o')

        plt.savefig(join(self.outs_dir,'disp_interpolation.png'))
        # plt.show()
        plt.close()

    def test_velocity_interpolation(self):
        fn = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        reader = vj.inv.ResultFileReader(fn)
        arr = reader.get_pred_disp()

        arr.set_mask_sites(['J550'])

        disp = []
        epochs = range(1,1200)
        for epoch in epochs:
            tp = arr.get_velocity_at_epoch(epoch)
            disp.append(tp[0])

        plt.plot(epochs, disp)

        disp = []
        epochs = arr.get_epochs()
        for epoch in epochs[1:]:
            tp = arr.get_velocity_at_epoch(epoch)
            disp.append(tp[0])

        plt.plot(epochs[1:], disp,'o')


        plt.savefig(join(self.outs_dir,'vel_interpolation.png'))
        # plt.show()
        plt.close()


if __name__ == '__main__':
    unittest.main()




