import unittest
import os
from os.path import join

from numpy import ones
from numpy.testing import assert_array_equal

from viscojapan.epochal_data.epochal_data import EpochalData
from viscojapan.test_utils import MyTestCase

class TestEpochalData(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.clean_outs_dir()

    def test_write_read_at_epoch(self):
        # write data at epoch:
        file = join(self.outs_dir, 'file.h5')
        ep = EpochalData(file)
        for n in range(10):
            ep[n] = n

        # read data at epoch and compare:
        file = join(self.outs_dir, 'file.h5')
        ep = EpochalData(file)
        for n in range(10):
            self.assertEqual(ep[n],n)

    def test_write_read_info(self):
        # write info:
        file = join(self.outs_dir, 'file.h5')
        ep = EpochalData(file)
        for n in range(10):
            ep['%04d'%n] = n

        # read info at epoch and compare:
        file = join(self.outs_dir, 'file.h5')
        ep = EpochalData(file)
        for n in range(10):
            self.assertEqual(ep['%04d'%n],n)
        
if __name__ == '__main__':
    unittest.main()
