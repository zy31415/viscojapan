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

        gmt.gplt.psbasemap(
            R = '5/15/52/58',       # region
            J = 'B10/55/55/60/10c', # projection
            B = '4g4',
            K = '')

        gmt.gplt.pscoast(
            R = '',
            J = '',
            D = 'f',
            W = 'thinnest',
            O = '')

        gmt.save(join(self.outs_dir, 'out.pdf'))
        gmt.save_shell_script(join(self.outs_dir, 'shell.sh'), output_file='>out.ps')
        
    
if __name__ == '__main__':
    unittest.main()
