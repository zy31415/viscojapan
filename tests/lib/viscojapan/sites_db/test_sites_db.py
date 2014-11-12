import unittest
from os.path import join

import viscojapan as vj
from viscojapan.test_utils import MyTestCase


class TestSites(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test_get_pos_dic(self):
        sites_dic = vj.sites_db.get_pos_dic()

    def test_get_networks_dic(self):
        networks_dic = vj.sites_db.get_networks_dic()
        #print(networks_dic.keys())


if __name__=='__main__':
    unittest.main()
    
