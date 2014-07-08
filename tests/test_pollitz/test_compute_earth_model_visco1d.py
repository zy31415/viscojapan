import unittest
from os.path import join

from viscojapan.test_utils import MyTestCase
from viscojapan.pollitz.compute_earth_model_visco1d \
     import ComputeEarthModelVISCO1D

class Test_gen_subflts_input_for_pollitz(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        com = ComputeEarthModelVISCO1D(
            earth_file = join(self.share_dir, 'earth.model'),
            l_max = 3,
            outputs_dir = join(self.outs_dir, 'earth_files')
            )
        com.run()


if __name__ == '__main__':
    unittest.main()

