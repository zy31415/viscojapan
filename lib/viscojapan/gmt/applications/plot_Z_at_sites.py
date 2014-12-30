import tempfile

from ...sites_db import get_pos
from .plotter import Plotter
from ..gadgets import plot_focal_mechanism_JMA

__all__ = ['ZPlotter']

class ZPlotter(Plotter):
    def __init__(self,
                 sites,
                 Z,
                 ):
        super().__init__()
        self.sites = sites
        self.lons, self.lats = get_pos(sites)
        
        self.Z = Z

    

    def plot(self, clim=[-2.5,1.1]):
        gmt = self.gmt

        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = gmt.gplt

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

        cpt = tempfile.NamedTemporaryFile('w+t')

        dcolor = (clim[1] - clim[0])/50
        gmt.makecpt(
            C='hot',
            T='{clim[0]}/{clim[1]}/{dcolor}'.format(clim=clim, dcolor=dcolor),
            I='', Q='',
            )

        gmt.save_stdout(cpt.name)

        with tempfile.NamedTemporaryFile('w+t') as fid:
            for zi, lon, lat in zip(self.Z, self.lons, self.lats):
                fid.write('%f %f %f\n'%(lon, lat, zi))
            fid.seek(0)
            gplt.psxy(
                fid.name,
                S = 'c.15',
                R='', J='', O='' ,K='',
                C=cpt.name)

        gplt.psscale(
            D='3/10/3/.15',
            R='', O='', K='',
            B='af',
            C=cpt.name, Q=''
            )

        cpt.close()
        
        plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

        
    
