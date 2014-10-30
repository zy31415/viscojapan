import unittest
from os.path import join

from numpy import asarray, arange
from numpy.testing import assert_array_almost_equal

from viscojapan.earth_model import EarthModelFileReader
from viscojapan.earth_model.plot_earth_model\
     import plot_earth_model_file_depth_change
from viscojapan.test_utils import MyTestCase


class Test_EarthModelFileReader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.earth_file = join(self.share_dir, 'earth.model_He50')
        self.em = EarthModelFileReader(self.earth_file)

    def test_get_shear_modulus(self):
        dep = arange(3, 50)
        # for ndarray
        visM = self.em.get_visM_by_dep(dep)
        print(self.em.visM)

        # for scalar:
        visM = self.em.get_visM_by_dep(dep[0])

    def test_plot_earth_model_file_depth_change(self):
        plot_earth_model_file_depth_change(
            self.earth_file,
            join(self.outs_dir, 'earth_model'),
            'pdf')

if __name__=='__main__':
    unittest.main()
