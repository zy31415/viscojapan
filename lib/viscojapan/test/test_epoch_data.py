import sys
from os.path import exists
import os
import unittest

from numpy import ones
from numpy.testing import assert_array_equal

from viscojapan.epochal_data.epochal_data import EpochalData


def deleteIfExists(fn):
    if exists(fn):
        os.remove(fn)

class TestEpochalData(unittest.TestCase):
    def set_epoch_value(self):
        epochs = range(1, 10)
        ep = EpochalData(self.epoch_file)
        for epoch in epochs:
            ep.set_epoch_value(epoch, epoch*ones((10,1)))

        self.ep = ep

    def set_info(self):
        sites0 = [b'a',b'b',b'c',b'd',b'e',
                  b'f',b'g',b'h',b'i']
        
        self.ep.set_info('sites',sites0,unit = 'meter')
        self.sites0 = sites0

    def setUp(self):
        self.epoch_file = 'test1.h5'
        deleteIfExists(self.epoch_file)

        self.set_epoch_value()
        self.set_info()

    def test_get_epochs(self):
        ep = self.ep
        epochs = ep.get_epochs()

        for epoch in epochs:
            val = ep.get_epoch_value(epoch)
            test_val = epoch*ones((10,1)).reshape([-1,1])
            assert_array_equal(val, test_val, verbose=True)

    def test_get_info(self):
        sites = self.ep.get_info('sites')
        for site1, site2 in zip(self.sites0, sites):
            self.assertEqual(site1,site2)

    def test_has_info(self):
        self.assertTrue(self.ep.has_info('sites'))
        self.assertFalse(self.ep.has_info('xxxx'))

    def tearDown(self):
        os.remove(self.epoch_file)

if __name__== '__main__':
    unittest.main()
