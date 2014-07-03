from os.path import join

from numpy import loadtxt
from pylab import plt

from .my_basemap import MyBasemap
from ..utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

class MapPlotSlab(object):
    def __init__(self, basemap=None):
        self.file_kur_top = join(this_script_dir, 'slab1.0/kur_top.in')
        self.basemap = basemap

        self.if_init = False
        
    def _init(self):
        if self.basemap is None:
            self.basemap = MyBasemap()
        self.basemap.init()
        self.if_init = True
        
    def plot_top(self):
        if not self.if_init:
            self._init()
            
        tp = loadtxt(self.file_kur_top)
        lon = tp[:,0]
        lat = tp[:,1]
        self.basemap.plot(lon,lat,latlon=True)
                                 



