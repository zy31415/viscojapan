import unittest
from os.path import join

from viscojapan.fault_model.fault_file_io import FaultFileReader
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_FaultFileWriter_FaultFileReader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)
        self.clean_outs_dir()

    def test_FaultFileReader(self):
        with FaultFileReader(join(self.share_dir, 'fault_bott50km.h5')) as w:
            self.assertEqual(w.num_subflt_along_strike, 35)
            self.assertEqual(w.num_subflt_along_dip, 11)


if __name__=='__main__':
    unittest.main()
