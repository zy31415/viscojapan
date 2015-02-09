import unittest
from os.path import join

import viscojapan as vj

class TestSites(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
    def test_save_sites_to_txt(self):
        sites = ['J550', 'J551', '_FUK']
        sites = vj.sites_db.SitesDB().gets(sites)

        # test save txt
        sites.save_to_txt(
            fn = join(self.outs_dir, 'sites.txt'),
            cols = 'id lon lat'
            )

    def test_lons_lats(self):
        sites = ['J550', 'J551', '_FUK']
        sites = vj.sites_db.SitesDB().gets(sites)

        sites.lons
        sites.lats

    def test_lon_lat_range(self):
        sites = ['J550', 'J551', '_FUK']
        sites = vj.sites_db.SitesDB().gets(sites)
        print(sites.max_lon, sites.min_lon)
        print(sites.max_lat, sites.min_lat)


if __name__=='__main__':
    unittest.main()
    
