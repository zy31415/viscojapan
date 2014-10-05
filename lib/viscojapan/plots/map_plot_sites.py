from os.path import join

#from scipy.interpolate import griddata
from pylab import plt
from matplotlib.mlab import griddata
from numpy import loadtxt
import numpy as np
from pylab import quiverkey

import viscojapan as vj

from .map_plot import MapPlot

from ..utils import get_this_script_dir
from ..epochal_data import EpochalDisplacement, EpochalG

this_file_path = get_this_script_dir(__file__)

__all__ = ['MapPlotDisplacement']

def ch_sub_set(set0, subset):
    set1 = list(set0)
    ch = np.asarray([False]*len(set0))
    if subset is not None:            
        for si in subset:
            if si in set0:
                idx = set1.index(si)
                ch[idx]=True
    return ch
    

class MapPlotDisplacement(MapPlot):
    def __init__(self,
                 basemap=None):
        super().__init__(basemap=basemap)
    
    def plot_disp(self,d,sites, sites_subset=None,
                  X=0.1,Y=0.1,U=1.,label='1m',
                  color='black',scale=None):
        ''' Plot displacment
'''
            
        lons,lats=vj.get_pos(sites)
        es=d[0::3]
        ns=d[1::3]
        us=d[2::3]

        if sites_subset is not None:
            ch = ch_sub_set(sites, sites_subset)
            lons = lons[ch]
            lats = lats[ch]
            es = es[ch]
            ns = ns[ch]
        
        Qu = self.basemap.quiver(lons,lats,es,ns,
                color=color,scale=scale,edgecolor=color,latlon=True)
            
        qk = quiverkey(Qu,X,Y,U,label,
                            labelpos='N')


    def plot_sites(self, sites,
                   marker='s', color='white', ms=5, text=True, fs=8):
        lons,lats=vj.get_pos(sites)
        self.basemap.plot(lons,lats, linestyle='None', 
                          marker=marker, color=color, ms=ms, latlon=True)
        if text:
            x,y = self.basemap(lons,lats)
            for xi, yi, ti in zip(x,y,sites):
                plt.text(xi+10, yi+15, ti.decode(), fontsize=fs)
            

    def plot_sites_seafloor(self, sites_file=None, sites_seafloor=None):
        if sites_file is None:
            sites_seafloor = vj.get_sites_seafloor()
        self.plot_sites(sites_seafloor,
                   marker='s', color='white', ms=5)
        
    def plot_disp_file(self, f_disp, epoch):
        disp_obj = EpochalDisplacement(f_disp)
        disp = disp_obj(epoch)
        sites = disp_obj.get_info('sites')
        self.plot_disp(disp, sites)

    def plot_G_file(self, f_G, epoch, mth, **kwargs):
        g = EpochalG(f_G)
        G = g[epoch]
        sites = g.get_info('sites')
        self.plot_disp(G[:,mth],sites, **kwargs)

    def plot_G_file_vis(self, f_G, epoch, mth, **kwargs):
        g = EpochalG(f_G)
        G0 = g[0]
        G = g[epoch] - G0
        sites = g.get_info('sites')
        self.plot_disp(G[:,mth],sites, **kwargs)

    def plot_scalor(self, z, sites, zorder=-2, **kwargs):
        lons,lats=vj.get_pos(sites)
        npts = 100
        xi = np.linspace(lons.min(), lons.max(), npts)
        yi = np.linspace(lats.min(), lats.max(), npts)

        zi = griddata(lons, lats, z, xi[None,:], yi[:,None])        
        im = self.basemap.pcolor(xi, yi, zi, latlon=True, zorder=zorder, **kwargs)
        return im
        
        
        
        
    
