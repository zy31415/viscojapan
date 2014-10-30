import unittest
import os
from os.path import join

from numpy import ones
from numpy.testing import assert_array_equal

from viscojapan.epochal_data.epochal_file_io import EpochalFileWriter, \
     EpochalFileReader
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import delete_if_exists
class TestEpochalData(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_EpochalFileWriter(self):
        # write data at epoch:
        file = join(self.outs_dir, 'file1.h5')
        delete_if_exists(file) 
        with EpochalFileWriter(file) as writer:
            for n in range(0, 10):
                writer.set_epoch_value(n, ones((10,1))*n)

        # use index
        file = join(self.outs_dir, 'file2.h5')
        delete_if_exists(file)
        with EpochalFileWriter(file) as writer:
            for n in range(0, 10):
                writer[n] = ones((10,1))*n**2
                writer['%04d'%n] = 'info %d'%n

    def test_EpochalFileReader(self):
        file = join(self.share_dir, 'sites_data.h5')
        with EpochalFileReader(file) as reader:
            for n in range(1, 10):
                reader.get_epoch_value(n)
                reader[n]
            reader['sites']

        
if __name__ == '__main__':
    unittest.main()
