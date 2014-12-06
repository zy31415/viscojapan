import pGMT

from ..gadgets import plot_etopo1, plot_slab,\
     plot_fault_model, plot_seafloor_stations, \
     plot_GEONET_Japan_stations, \
     plot_focal_mechanism_USGS_wphase

__all__ = ['FaultModelPlotter']

class FaultModelPlotter(object):
    def __init__(self,
                 fault_file
                 ):
        self.fault_file = fault_file
        

    def plot(self, output_file):
        gmt = pGMT.GMT()
        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'MAP_FRAME_TYPE','plain',
                   )
        

        gplt = gmt.gplt

        gplt.psbasemap(
            R = '138/146/33.5/42',       # region
            J = 'B141.5/38.5/33.5/42/15c', # projection
            B = '2', U='20/0/22/Yang', P='', K=''
            )

        plot_etopo1(gplt)
        plot_slab(gplt)

        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,50,--',
            W = 'faint,100', L='f145/34/38/100+lkm+jt',
            O = '', K='')

        plot_fault_model(gplt,self.fault_file)
        plot_seafloor_stations(gplt, marker_size=0.4,color='red')
        plot_GEONET_Japan_stations(gplt, color='red')

        plot_focal_mechanism_USGS_wphase(gplt,K=None)

        gmt.save(output_file)
