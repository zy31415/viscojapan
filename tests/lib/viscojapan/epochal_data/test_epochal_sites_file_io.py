import unittest
import os
from os.path import join

from numpy import loadtxt
from numpy.testing import assert_equal, assert_array_equal

from viscojapan.epochal_data.epochal_sites_file_io import EpochalSitesFileReader

from viscojapan.test_utils import MyTestCase

from test_utils import create_a_sites_data_file


class Test_EpochalSitesFileReader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.sites_data_file = join(self.share_dir,'sites_data.h5')
        create_a_sites_data_file(self.sites_data_file)
        
        self.filter_sites_file = join(self.share_dir,'filter_sites')
        self.filter_sites = loadtxt(self.filter_sites_file,'4a')
        self.num_of_sites = len(self.filter_sites)

    def test1(self):
        reader = EpochalSitesFileReader(join(self.share_dir,'sites_data.h5'))
        self.assertEqual(reader.all_sites, reader.filter_sites)

    def test2(self):
        reader = EpochalSitesFileReader(
            join(self.share_dir,'sites_data.h5'),
            join(self.share_dir,'filter_sites')
            )
        # print(reader.filter_sites)
        

if __name__== '__main__':
    unittest.main()
