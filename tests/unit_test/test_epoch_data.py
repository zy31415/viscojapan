import unittest
import os

from numpy import ones
from numpy.testing import assert_array_equal

from viscojapan.epochal_data.epochal_data import EpochalData
from .test_utils import create_a_sites_data_file

class TestEpochalData(unittest.TestCase):
    def setUp(self):
        self.sites_data_file = 'sites_data.h5'
        create_a_sites_data_file(self.sites_data_file)
        self.ep = EpochalData(self.sites_data_file)

    def test_get_epochs(self):
        ep = self.ep
        epochs = ep.get_epochs()

    def test_get_info(self):
        sites = self.ep.get_info('sites')


    def test_has_info(self):
        self.assertTrue(self.ep.has_info('sites'))
        self.assertFalse(self.ep.has_info('xxxx'))

    def tearDown(self):
        os.remove(self.sites_data_file)

if __name__== '__main__':
    unittest.main()
