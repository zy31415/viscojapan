from os.path import join
import re

from numpy import loadtxt
from pylab import plt

from .map_plot import MapPlot
from ..utils import get_this_script_dir, kw_init

this_script_dir = get_this_script_dir(__file__)

class MapPlotSlab(MapPlot):
    def __init__(self, basemap=None, **kwargs):
        super().__init__(basemap = basemap)
        self.file_kur_top = join(this_script_dir,
                                 'share/slab1.0/kur_top.in')
        self.file_dep_contour = join(this_script_dir,
                                     'share/slab1.0/kur_contours.in')
        kw_init(self, kwargs)
        
    def plot_top(self):        
        tp = loadtxt(self.file_kur_top)
        lon = tp[:,0]
        lat = tp[:,1]
        self.basemap.plot(lon,lat,latlon=True)

    def plot_dep_contour(self, dep, ms=2, **kwargs):
        tp = loadtxt(self.file_dep_contour, comments='>')
        ch = (tp[:,2] < dep+0.1) & (tp[:,2] > dep - 0.1)
        if not any(ch):
            raise ValueError('No such depth!')
        arr = tp[ch,:]
        lons = arr[:,0]
        lats = arr[:,1]
        self.basemap.plot(lons,lats,latlon=True,
                          marker='.',ls='',ms=ms, **kwargs)
                                 



