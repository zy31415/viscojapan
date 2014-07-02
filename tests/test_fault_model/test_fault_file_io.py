import unittest
from os.path import join

from viscojapan.fault_model.fault_file_io import FaultFileIO
from viscojapan.utils import get_this_script_dir

this_file_path = get_this_script_dir(__file__)

class TestFaultFileIO(unittest.TestCase):
    def setUp(self):
        self.fault_file = join(this_file_path, 'subfaults.h5')

    def test(self):
        fio = FaultFileIO(self.fault_file)
        res = fio.num_subflt_along_strike


if __name__=='__main__':
    unittest.main()
