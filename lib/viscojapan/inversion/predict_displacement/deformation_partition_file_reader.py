from os.path import exists

import h5py
import numpy as np

from ...displacement import Disp
from ..result_file import ResultFileReader
from ...sites import Site

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

    def _read(self, cmpt):
        with h5py.File(self.fn,'r') as fid:
            disp3d = fid[cmpt][...]
            sites = fid['sites'][...]
            epochs = fid['epochs'][...]

        sites = [Site(site.decode()) for site in sites]

        return Disp(cumu_disp3d=disp3d,
             epochs=epochs,
             sites=sites
        )

    def check_partition_result(self, result_file):

        pred = ResultFileReader(result_file).get_pred_disp().cumu3d

        Ecumu = self.Ecumu.cumu3d
        Rco = self.Rco.cumu3d
        Raslip = self.Raslip.cumu3d

        np.testing.assert_array_almost_equal(pred, Ecumu+Rco+Raslip, decimal=1)

        print('Pass checking! Prediction equals components added!')