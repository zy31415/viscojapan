from os.path import exists

import h5py
import numpy as np

from ...epoch_3d_array import Displacement

from ..result_file import ResultFileReader

__author__ = 'zy'
__all__ = ['DeformPartitionResultReader']

class DeformPartitionResultReader(object):
    def __init__(self, fn):
        self.fn = fn
        assert exists(self.fn), "File %s doesn't exist!"%self.fn

    @property
    def Rco(self):
        return self._read('Rco')

    @property
    def Raslip(self):
        return self._read('Raslip')

    @property
    def Ecumu(self):
        return self._read('Ecumu')

    @property
    def d_added(self):
        return self._read('d_added')

    def _read(self, cmpt, sites='sites_for_prediction'):
        with h5py.File(self.fn,'r') as fid:
            disp3d = fid[cmpt][...]
            sites = fid[sites][...]
            epochs = fid['epochs'][...]

        sites = [site.decode() for site in sites]

        return Displacement(cumu_disp_3d=disp3d,
             epochs=epochs,
             sites=sites
        )

    @property
    def sites(self):
        with h5py.File(self.fn,'r') as fid:
            sites = fid['sites_for_prediction'][...]
        sites = [site.decode() for site in sites]
        return sites

    def check_partition_result(self, result_file):
        result_reader = ResultFileReader(result_file)
        disp_pred = result_reader.get_pred_disp()
        pred = disp_pred.get_cumu_disp_3d()

        sites = result_reader.sites

        tp = self.Ecumu
        tp.set_mask_sites(sites)
        Ecumu =  tp.get_cumu_disp_3d()

        tp = self.Rco
        tp.set_mask_sites(sites)
        Rco = tp.get_cumu_disp_3d()

        tp = self.Raslip
        tp.set_mask_sites(sites)
        Raslip = tp.get_cumu_disp_3d()

        np.testing.assert_array_almost_equal(pred, Ecumu+Rco+Raslip)

        print('Pass checking! Prediction equals components added!')