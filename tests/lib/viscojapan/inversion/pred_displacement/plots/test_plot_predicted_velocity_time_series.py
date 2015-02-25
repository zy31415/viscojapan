__author__ = 'zy'

import unittest
from os.path import join

from pylab import plt

import viscojapan as vj

class Test_PredictedVelocityTimeSeriesPlotter(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        partition_file = '/home/zy/workspace/viscojapan/tests/share/deformation_partition.h5'

        plotter = vj.inv.PredictedVelocityTimeSeriesPlotter(
            partition_file = partition_file
            )

        site = 'J550'
        cmpt = 'e'

        plotter.plot_vel_decomposition(site, cmpt)
        plt.show()
        plt.close()



        



if __name__ == '__main__':
    unittest.main()
