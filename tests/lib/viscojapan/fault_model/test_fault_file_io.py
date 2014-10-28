import unittest
from os.path import join

from viscojapan.fault_model.fault_file_io import FaultFileIO
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class TestFaultFileIO(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)
        
        self.fault_file = join(self.share_dir, 'subfaults.h5')

    def test(self):
        fio = FaultFileIO(self.fault_file)
        res = fio.num_subflt_along_strike


if __name__=='__main__':
    unittest.main()
