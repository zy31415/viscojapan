__author__ = 'zy'

import unittest
from os.path import join

from pylab import plt

import viscojapan as vj

class Test_PredictedTimeSeriesPlotter(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        partition_file = '/home/zy/workspace/viscojapan/tests/share/deformation_partition.h5'
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'



        plotter = vj.inv.PredictedTimeSeriesPlotter(
            partition_file = partition_file,
            result_file = res_file,
            )

        site = 'J550'
        cmpt = 'e'
        #plotter.plot_cumu_disp_pred(site, cmpt)
        #plotter.plot_cumu_disp_pred_added(site, cmpt, color='blue')
        # plotter.plot_post_disp_pred_added(site, cmpt)
        #plotter.plot_cumu_obs_linres(site, cmpt)
        #plotter.plot_R_co(site, cmpt)
        # plotter.plot_post_disp_pred(site, cmpt)
        # plotter.plot_post_obs_linres(site, cmpt)
        #plotter.plot_E_cumu_slip(site, cmpt)
        # plotter.plot_E_aslip(site, cmpt)
        #plotter.plot_R_aslip(site, cmpt)
        #plt.show()
        #plt.close()

        plotter.plot_cumu_disp_decomposition(site, cmpt)
        plotter.plot_cumu_disp_pred_added(site, cmpt, color='blue')
        plt.show()
        plt.close()
        #
        # plotter.plot_post_disp(site, cmpt)
        # plt.show()
        # plt.close()


        



if __name__ == '__main__':
    unittest.main()
