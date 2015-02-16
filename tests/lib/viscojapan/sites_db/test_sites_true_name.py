import unittest
from os.path import join

import viscojapan as vj
from viscojapan.test_utils import MyTestCase


class Test_sites_true_name(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test(self):
        reader = vj.sites_db.SitesDB()
        sites = ['J550','J460']
        
        names = vj.sites_db.get_sites_true_name(sites_ids=sites)
        #print(names)

    
if __name__=='__main__':
    unittest.main()
    
