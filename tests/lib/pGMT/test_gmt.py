import unittest
from os.path import join

from viscojapan.test_utils import MyTestCase

import pGMT

class Test_GMT(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        gmt = pGMT.GMT()
        gmt.ls(1,2,s=3,b=5)
        
    
if __name__ == '__main__':
    unittest.main()
