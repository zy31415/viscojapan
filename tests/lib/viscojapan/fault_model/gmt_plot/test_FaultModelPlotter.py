import unittest
from os.path import join

import viscojapan as vj

from viscojapan.test_utils import MyTestCase

class Test_FaultModelPlotter(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)
        self.clean_outs_dir()

    def test(self):
        fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5'
        plt = vj.fm.gmt_plot.FaultModelPlotter(fault_file)
        plt.plot()
        plt.save(join(self.outs_dir,'fault_model.pdf'))



if __name__=='__main__':
    unittest.main()
