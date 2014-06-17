import unittest
import multiprocessing
import sys

from numpy.testing import assert_array_equal
from numpy import asarray
from nose.plugins.attrib import attr
import pytest

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.epochal_data.stacking import conv_stack, conv_stack_sparse
from viscojapan.epochal_data.epochal_data import EpochalData
from viscojapan.utils import timeit

@pytest.mark.skipif(multiprocessing.cpu_count() < 10,
                    reason="Large memory (e.g. server) needed Server needed to run this test. ")
class TestConvStacking(unittest.TestCase):
    def setUp(self):
        self.G_file = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        self.ep_obj = EpochalData(self.G_file)
        self.epochs = range(20)

    @timeit
    def test_conv_stack(self):
        res = conv_stack(self.ep_obj, self.epochs)
        print(['x']*1000)

    @timeit
    def test_conv_stack_sparse(self):
        res = conv_stack_sparse(self.ep_obj, self.epochs)

    @attr('slow')
    def test_conv_stack_EQUALITY(self):
        res1 = conv_stack(self.ep_obj, self.epochs)
        res2_sparse = conv_stack_sparse(self.ep_obj, self.epochs)
        res2 = res2_sparse.todense()
        assert_array_equal(res1,res2)
        
    def tearDown(self):
        pass

if __name__=='__main__':
    unittest.main()
