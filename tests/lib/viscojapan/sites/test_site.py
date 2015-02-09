import unittest
from os.path import join

import viscojapan as vj

class TestSites(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
    def test_Site(self):
        site1 = vj.sites_db.SitesDB().get('ULAB')
        site2 = vj.sites_db.SitesDB().get('J550')
        site1 == site2


if __name__=='__main__':
    unittest.main()
    
