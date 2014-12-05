import tempfile

import numpy as np

from ..utils import plot_seafloor_stations, plot_slab
from ..plot_focal_mechanism import plot_focal_mechanism_USGS_wphase

class PlotSlip(object):
    def __init__(self,
                 gmt,
                 lons,
                 lats,
                 slip,
                 cpt_file,
                 offset_X = 0,
                 offset_Y = 0,
                 size = '4c',
                 if_boundary_annotation = False,
                 if_map_scale = False,
                 if_slab_annotation = False,
                 if_psscale = False,
                 psscale_gridline_interval = '3',
                 O = None,
                 K = ''
                 ):
        self.gmt = gmt
        self.gplt = gmt.gplt

        self.lons = lons
        self.lats = lats
        self.slip = slip

        self.cpt_file = cpt_file
        
        self.offset_X = offset_X
        self.offset_Y = offset_Y

        self.size = size

        self.if_boundary_annotation = if_boundary_annotation 
        self.if_map_scale = if_map_scale
        self.if_slab_annotation = if_slab_annotation
        self.if_psscale = if_psscale
        self.psscale_gridline_interval = psscale_gridline_interval
        self.O = O
        self.K = K

    def _form_slip_xyz_file_string(self):
        _txt = ''
        for lon, lat, s in zip(np.nditer(self.lons),
                               np.nditer(self.lats),
                               np.nditer(self.slip)):
            _txt +='%f %f %f\n'%(lon, lat, s)
        return _txt
        
    def plot(self):
        gmt = self.gmt
        gplt = self.gplt

        if self.if_boundary_annotation:
            B = '2WENS'
        else:
            B = '2wens'

        gplt.psbasemap(
        R = '140/145/35/41.5',       # region
        JB = '142.5/38.5/35/41.5/%s'%self.size, # projection
        B = B, U='18/25/0',
        P='',K='', O=self.O,
        X = self.offset_X,
        Y = self.offset_Y,
        )

        grd_file = tempfile.NamedTemporaryFile()
        
        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write(self._form_slip_xyz_file_string())
            fid.seek(0,0)
            gmt.nearneighbor(
                fid.name,
                R='',
                I='2k',
                G = grd_file.name,
                N='8',
                S='40k')

            gplt.grdimage(
                grd_file.name,
                J='', R='', C=self.cpt_file,
                O='',K='', Q='',            
                )
        grd_file.close()

        if self.if_map_scale:
            L = '144.4/35.6/38/50+lkm+jt'
        else:
            L = None
            
        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,150,-.',
            W = 'faint,dimgray',A='1000',L=L,
            O = '', K='')

        if self.if_psscale:                
            gplt.psscale(
            D = '.5/3.5/1.6/.1',
            B = '%s::/:m:'%self.psscale_gridline_interval,
            O = '', K='',
            C = self.cpt_file)

        plot_seafloor_stations(gplt, marker_size=0.1,
                                      lw='faint',color='green')

        plot_focal_mechanism_USGS_wphase(gplt,scale=0.1, fontsize=0)
        plot_slab(gplt,
                         color='dimgray', lw='faint',
                         label_line = '144/41/138/41',
                         label_font_size = '4',
                         label_color = 'dimgray',
                         K = self.K,
                         if_contour_annotation = self.if_slab_annotation
                         )

        

