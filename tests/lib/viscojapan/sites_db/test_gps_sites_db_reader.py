import unittest
from os.path import join

import viscojapan as vj
from viscojapan.test_utils import MyTestCase


class TestSites(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test_SitesDBReader_get(self):
        reader = vj.sites_db.SitesDB()
        reader.get('J550')

    def test_SitesDBReader_gets(self):
        reader = vj.sites_db.SitesDB()
        sites = reader.gets(['J550','J460'])
##        for site in sites:
##            print(site)

    def test_sitesDBReader_gets(self):
        sites = vj.sites_db.sitesDBReader.gets(['J550','J460'])
        for site in sites:
            print(site)


if __name__=='__main__':
    unittest.main()
    
