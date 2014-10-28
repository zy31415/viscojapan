import unittest
from os.path import join

from viscojapan.test_utils import MyTestCase
from viscojapan.earth_model import GenerateEarthModelFile, raw_file_He50km

class Test_GenEarthModelFile(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_GenEarthModelFile(self):
        gen = GenerateEarthModelFile(
            raw_file_He50km,
            50,
            )
        print(gen.gen_earthmodel_file())
        gen.save(join(self.outs_dir, 'earth.model'))
    


if __name__=='__main__':
    unittest.main()
