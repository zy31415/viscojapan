import unittest
import os
from os.path import join

from numpy import loadtxt
from numpy.testing import assert_equal, assert_array_equal

from viscojapan.epochal_data.epochal_sites_data import EpochalSitesFilteredData
from viscojapan.test_utils import MyTestCase

from test_utils import create_a_sites_data_file


class TestEpochalSitesFilteredData(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.sites_data_file = join(self.share_dir,'sites_data.h5')
        create_a_sites_data_file(self.sites_data_file)
        
        self.filter_sites_file = join(self.share_dir,'filter_sites')
        self.filter_sites = loadtxt(self.filter_sites_file,'4a')
        self.num_of_sites = len(self.filter_sites)

    def test_create_EpochalSitesFilteredData_1(self):
        sites_data_obj = EpochalSitesFilteredData(self.sites_data_file,
                                                  self.filter_sites_file)
    def test_create_EpochalSitesFilteredData_2(self):
        sites_data_obj = EpochalSitesFilteredData(self.sites_data_file)

        sites = sites_data_obj.sites
        filter_sites = sites_data_obj.filter_sites

        assert_array_equal(sites, filter_sites)

        sites_data_obj.filter_sites = sites[0:3]

        value = sites_data_obj.get_epoch_value(1)
        self.assertEqual(len(value), 9)
        

if __name__== '__main__':
    unittest.main()
