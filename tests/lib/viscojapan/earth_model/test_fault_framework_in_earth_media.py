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
        # for ndarray
        visM = self.em.get_visM_by_dep(dep)
        print(self.em.visM)

        # for scalar:
        visM = self.em.get_visM_by_dep(dep[0])        

if __name__=='__main__':
    unittest.main()
