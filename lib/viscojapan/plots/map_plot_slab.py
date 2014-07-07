from os.path import join

from numpy import loadtxt
from pylab import plt

from .map_plot import MapPlot
from ..utils import get_this_script_dir, kw_init

this_script_dir = get_this_script_dir(__file__)

class MapPlotSlab(MapPlot):
    def __init__(self, **kwargs):
        super().__init__()
        self.file_kur_top = join(this_script_dir, 'share/slab1.0/kur_top.in')
        
        kw_init(self, kwargs)
        
    def plot_top(self):        
        tp = loadtxt(self.file_kur_top)
        lon = tp[:,0]
        lat = tp[:,1]
        self.basemap.plot(lon,lat,latlon=True)
                                 



