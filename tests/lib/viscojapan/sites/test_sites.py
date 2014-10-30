import unittest
from os.path import join

from viscojapan.sites.sites import *
from viscojapan.sites.sites import SitePosDictSingleton
from viscojapan.test_utils import MyTestCase


class TestSites(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test_SitePosDictSingleton(self):
        s1 = SitePosDictSingleton()
        s2 = SitePosDictSingleton()
        self.assertEqual(s1, s2)

        s1.names

    def test_Site(self):
        # seafloor or onshore?
        s1 = Site('J550')
        self.assertTrue(s1.if_onshore)
        self.assertFalse(s1.if_seafloor)

        s2 = Site('_FUK')
        self.assertFalse(s2.if_onshore)
        self.assertTrue(s2.if_seafloor)

        # test __str__
        print(s1)
        print(s2)

        # test equality
        self.assertNotEqual(s1, s2)
        s3 = Site('_FUK')
        self.assertEqual(s3, s2)
        
    def test_Sites(self):
        sns = ['J550', 'J551', '_FUK']
        sites = Sites(sns)
        sites.names
        self.assertEqual(sites.names_onshore, ['J550', 'J551'])
        self.assertEqual(sites.names_seafloor,['_FUK'])

        # test save txt
        sites.save2txt(join(self.outs_dir, 'sites.txt'),
                       '# This is a header.')
        # test save to kml
        sites.save2kml(join(self.outs_dir, 'sites.kml'))

        # test all sites list:
        s = Sites.init_including_all()
        s.save2kml(join(self.outs_dir, 'sites.kml'))
        self.assertEqual(len(s), s.num_sites)

        # init from txt file:
        s = Sites.init_from_txt(join(self.share_dir, 'sites_with_seafloor'))




if __name__=='__main__':
    unittest.main()
    
