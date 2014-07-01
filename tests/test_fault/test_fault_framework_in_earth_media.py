import unittest

from numpy import asarray
from numpy.testing import assert_array_almost_equal

from viscojapan.fault.fault_framework_in_earth_media import \
     FaultFrameworkInEarthMedia

class TestFaultFrameworkInEarthMedia(unittest.TestCase):
    def setUp(self):
        self.fm = FaultFrameworkInEarthMedia()

    def test(self):
        dep = self.fm.DEP_SHEAR
        shear = self.fm.get_shear(dep)
        assert_array_almost_equal(shear, self.fm.SHEAR_MODULUS)
        

if __name__=='__main__':
    unittest.main()
