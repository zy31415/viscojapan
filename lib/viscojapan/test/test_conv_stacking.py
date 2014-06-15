import unittest

from numpy.testing import assert_array_equal
from numpy import asarray

from viscojapan.epochal_data.stacking import conv_stack, conv_stack_sparse
from viscojapan.epochal_data.epochal_data import EpochalData

class TestConvStacking(unittest.TestCase):
    def setUp(self):
        self.G_file = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        self.ep_obj = EpochalData(self.G_file)
        self.epochs = range(20)

    def test_conv_stack(self):
        res = conv_stack(self.ep_obj, self.epochs)

    def test_conv_stack_sparse(self):
        res = conv_stack_sparse(self.ep_obj, self.epochs)

    def test_conv_stack_EQUALITY(self):
        res1 = conv_stack(self.ep_obj, self.epochs)
        res2_sparse = conv_stack_sparse(self.ep_obj, self.epochs)
        res2 = res2_sparse.todense()
        assert_array_equal(res1,res2)
        
    def tearDown(self):
        pass

if __name__=='__main__':
    unittest.main()
