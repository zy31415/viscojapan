import unittest
from os.path import join

import viscojapan as vj

class Test_epicentral_distance(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
    def test_for_one_site(self):
        site = vj.sites_db.SitesDB().get('ULAB')
        dis = vj.sites.get_epicentral_distance(site)
        print(dis)

    def test_for_sites(self):
        sites = vj.sites_db.SitesDB().gets(
            ['ULAB','J550'])
        dis = vj.sites.get_epicentral_distance(sites)
        print(dis)

    def test_for_sorting(self):
        sites = vj.sites_db.SitesDB().gets(
            ['J669','ULAB','J550'])
        sites_sorted, dist_sorted = vj.sites.sorted_by_epicentral_distance(
            sites)

if __name__=='__main__':
    unittest.main()
    
