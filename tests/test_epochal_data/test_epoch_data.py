import unittest
import os
from os.path import join

from numpy import ones
from numpy.testing import assert_array_equal

from viscojapan.epochal_data.epochal_data import EpochalData
from viscojapan.utils import get_this_script_dir, delete_if_exists
from test_utils import create_a_sites_data_file

this_test_path = get_this_script_dir(__file__)
class TestEpochalData(unittest.TestCase):
    def setUp(self):
        self.sites_data_file = join(this_test_path, 'sites_data.h5')
        delete_if_exists(self.sites_data_file)
        
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


if __name__== '__main__':
    unittest.main()
