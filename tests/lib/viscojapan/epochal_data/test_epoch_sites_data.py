import unittest
import os
from os.path import join

from numpy import loadtxt
from numpy.testing import assert_equal

from viscojapan.epochal_data.epochal_sites_data import \
     EpochalSitesData, EpochalSitesFilteredData, EpochalDisplacement
from viscojapan.test_utils import MyTestCase

from test_utils import create_a_sites_data_file


class TestEpochalSitesData(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.sites_data_file = join(self.share_dir, 'sites_data.h5')
        create_a_sites_data_file(self.sites_data_file)
        self.filter_sites_file = join(self.share_dir,'filter_sites')

    def test_EpochalSitesData(self):
        sites_data_obj = EpochalSitesData(self.sites_data_file)
        sites = sites_data_obj.sites

        idx = sites_data_obj.get_site_cmpt_idx('J550','e')
        self.assertEqual(idx, 2427)

        tp = sites_data_obj.get_epoch_value_at_site('J550','e',5)

    def test_EpochalDisplacement(self):
        obj = EpochalDisplacement(self.sites_data_file, self.filter_sites_file)
        ys = obj.get_time_series('G008','e')

    def test_set_epoch_value_at_site(self):
        sites_data_obj = EpochalSitesData(self.sites_data_file)
        test_val = 99999.
        sites_data_obj.set_value_at_site('019B','e',5, test_val)
        val = sites_data_obj.get_epoch_value_at_site('019B','e',5)

        assert_equal(test_val, val)
        
       
if __name__== '__main__':
    unittest.main()
