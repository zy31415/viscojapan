import unittest

import viscojapan as vj
from viscojapan.test_utils import MyTestCase


class Test_networks(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test(self):
        sites = vj.sites_db.get_sites_from_network('GEONET')
        print(sites)


if __name__=='__main__':
    unittest.main()
