import unittest
from os.path import join

import numpy as np

import viscojapan as vj

class Test_MagnitudeContours(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.clean_outs_dir()

    def test(self):
        pred = join(self.share_dir, 'deformation_partition_large_scale.h5')

        reader = vj.inv.DeformPartitionResultReader(pred)

        Ecumu = reader.Ecumu

        mags = Ecumu.get_post_hor_mag_at_epoch(111)
        
        tp = np.loadtxt(join(self.share_dir, 'stations_large_scale.in'), '4a,f,f')
        lons = [ii[1] for ii in tp]
        lats = [ii[2] for ii in tp]

        plt = vj.displacement.plot.MagnitudeContoursPlotter()
        plt.plot(lons, lats, mags, join(self.outs_dir, 'mags.pdf'))


if __name__=='__main__':
    unittest.main()

