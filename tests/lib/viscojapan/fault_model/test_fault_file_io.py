import unittest
from os.path import join

from viscojapan.fault_model.fault_file_io import FaultFileWriter
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_FaultFileWriter_FaultFileReader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)
        
        self.fault_file = join(self.share_dir, 'subfaults.h5')

    def test_FaultFileWriter(self):
        w = FaultFileWriter(join(self.outs_dir, 'subfaults.h5'))
        w.num_subflt_along_strike = 1
        w.num_subflt_along_dip = 2
        


if __name__=='__main__':
    unittest.main()
