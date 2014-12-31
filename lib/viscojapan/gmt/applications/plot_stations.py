from .plotter import Plotter
from ..gadgets import plot_stations, plot_focal_mechanism_JMA

__all__ = ['SitesPlotter']

class SitesPlotter(Plotter):
    def __init__(self):
        super().__init__()

    def plot(self, sites):
        gmt = self.gmt

        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = self.gplt

        gplt.psbasemap(
            R = '128/147/30/46',       # region
            JB = '137.5/38.5/35/41.5/14c', # projection
            B = '5', U='18/25/0',
            P='',K='',
            )

        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,150,-.',
            W = 'faint,dimgray',A='500',L='144/32/38/200+lkm+jt',
            O = '', K='')

        plot_stations(gplt, sites, S='c.05')

        plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

