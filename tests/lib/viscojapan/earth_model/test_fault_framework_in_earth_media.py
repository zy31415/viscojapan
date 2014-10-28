import unittest
from os.path import join

from numpy import asarray, arange
from numpy.testing import assert_array_almost_equal

from viscojapan.earth_model import EarthModelFileReader
from viscojapan.utils import get_this_script_dir

this_file_path = get_this_script_dir(__file__)

class TestEarthModel(unittest.TestCase):
    def setUp(self):
        self.earth_file = join(this_file_path, 'earth.model_He50')
        self.em = EarthModelFileReader(self.earth_file)

    def test_get_shear_modulus(self):
        dep = arange(3, 50)
        shear = self.em.get_shear_modulus(dep)
        

if __name__=='__main__':
    unittest.main()
