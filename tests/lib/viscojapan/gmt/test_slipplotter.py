import unittest
from os.path import join

from viscojapan.test_utils import MyTestCase
import viscojapan as vj

import pGMT

class Test_SlipPlotter(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        gmt = pGMT.GMT()
        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = pGMT.GMTPlot()

        gplt.psbasemap(
            R = '140/145/35/41.5',       # region
            JB = '142.5/38.5/35/41.5/14c', # projection
            B = '2', U='18/25/0',
            P='',K='',
            )
        plt_slip = vj.gmt.SlipPlotter(
            gplt,
            join(self.share_dir, 'coseismic_slip.txt')
            )
        plt_slip._workdir = join(self.outs_dir,'tmp')
        plt_slip.plot_slip()
        plt_slip.plot_slip_contour()
        plt_slip.plot_scale()

        # plot coast
        gplt.pscoast(
            R = '', J = '',
            D = 'l', N = 'a/faint,100,-.',
            W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
            O = '', K=None)

        gplt.save(join(self.outs_dir, 'inverted_coseismic_slip.pdf'))
        

        
    
if __name__ == '__main__':
    unittest.main()
