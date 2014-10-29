import unittest
from os.path import join

from viscojapan.fault_model.gen_kml_for_fault_file import gen_kml_for_fault_file
from viscojapan.test_utils import MyTestCase

class Test_FaultFileWriter_FaultFileReader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)
        self.clean_outs_dir()

    def test(self):
        fault_file = join(self.share_dir, 'fault_bott50km.h5')
        gen_kml_for_fault_file(
            fault_file,
            join(self.outs_dir, 'fault.kml'),
            )        


if __name__=='__main__':
    unittest.main()
