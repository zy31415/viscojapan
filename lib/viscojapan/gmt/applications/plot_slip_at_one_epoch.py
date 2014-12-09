
import pGMT

import viscojapan as vj

from .plotter import Plotter

__all__ = ['SlipAtOneEpochPlotter']

class SlipAtOneEpochPlotter(Plotter):
    def __init__(self,
                 result_file,
                 fault_file,
                 earth_file
                 ):
        super().__init__()
        self.result_file = result_file
        self.fault_file = fault_file
        self.earth_file = earth_file

        self.trash_files = ['gmt.conf', 'gmt.history']


    def plot(self, output_file):
        super().plot(output_file)
        gmt = pGMT.GMT()
        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = gmt.gplt

        gplt.psbasemap(
            R = '140/145/35/41.5',       # region
            JB = '142.5/38.5/35/41.5/14c', # projection
            B = '2', U='18/25/0',
            P='',K='',
            )

        vj.gmt.plot_etopo1(gplt, A='-80/10',
                           file_topo_cpt=vj.gmt.share.topo_cpts['afrikakarte'])
        plt_slip = vj.gmt.GMTInversionResultFileSlipPlotter(
            gplt,
            self.result_file,
            self.fault_file,
            self.earth_file,
            I='1k')
        plt_slip.plot_slip()
        plt_slip.plot_slip_contour()
        plt_slip.plot_scale()
        plt_slip.plot_legend()

        # plot coast
        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,150,-.',
            W = 'faint,50',A='1000',L='144.3/36/38/50+lkm+jt',
            O = '', K='')

        # plot plate boundary
        vj.gmt.plot_plate_boundary(gplt)
        # plot focal mechanism
        #vj.gmt.plot_focal_mechanism_CMT(gplt,scale=0.4, fontsize=0)
        #vj.gmt.plot_focal_mechanism_USGS_wphase(gplt,scale=0.4, fontsize=8)
        vj.gmt.plot_focal_mechanism_JMA(gplt,scale=0.4, fontsize=0, K=None)

        gmt.save('inverted_coseismic_slip.pdf')

        
        
    
