import unittest
import os
from os.path import join

from numpy import loadtxt

from viscojapan.epochal_data.epochal_sites_data import \
     EpochalSitesData, EpochalSitesFilteredData, EpochalDisplacement
from viscojapan.utils import get_this_script_dir, delete_if_exists

from test_utils import create_a_sites_data_file

this_test_path = get_this_script_dir(__file__)

class TestEpochalSitesData(unittest.TestCase):
    def setUp(self):
        self.sites_data_file = join(this_test_path, 'sites_data.h5')
        create_a_sites_data_file(self.sites_data_file)
        self.filter_sites_file = os.path.join(this_test_path,'filter_sites')

    def test_EpochalSitesData(self):
        sites_data_obj = EpochalSitesData(self.sites_data_file)
        sites = sites_data_obj.get_sites()

        idx = sites_data_obj.get_site_cmpt_idx('J550','e')
        self.assertEqual(idx, 2427)

        tp = sites_data_obj.get_epoch_value_at_site('J550','e',5)

    def test_EpochalDisplacement(self):
        obj = EpochalDisplacement(self.sites_data_file, self.filter_sites_file)
        ys = obj.get_time_series('G008','e')
        

class TestEpochalSitesFilteredData(unittest.TestCase):
    def setUp(self):
        self.sites_data_file = join(this_test_path,'sites_data.h5')
        create_a_sites_data_file(self.sites_data_file)
        self.filter_sites_file = os.path.join(this_test_path,'filter_sites')
        self.filter_sites = loadtxt(self.filter_sites_file,'4a')
        self.num_of_sites = len(self.filter_sites)

    def test(self):
        sites_data_obj = EpochalSitesFilteredData(self.sites_data_file,
                                                  self.filter_sites_file)

        epochs = sites_data_obj.get_epochs()
        for epoch in epochs:
            val = sites_data_obj.get_epoch_value(epoch)
            self.assertEqual(self.num_of_sites*3,len(val))

        for epoch in epochs[:-1]:
            val = sites_data_obj.get_epoch_value(epoch+0.1)
        
if __name__== '__main__':
    unittest.main()
