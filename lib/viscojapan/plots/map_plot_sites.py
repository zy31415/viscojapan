from os.path import join
from numpy import loadtxt
from pylab import quiverkey

import viscojapan as vj

from .map_plot import MapPlot

from ..utils import get_this_script_dir
from ..epochal_data import EpochalDisplacement, EpochalG

this_file_path = get_this_script_dir(__file__)

def get_pos_dic():
    ''' Return a dictionary of position of all stations.
'''
    tp=loadtxt(join(this_file_path, 'share/sites_with_seafloor'),'4a, 2f')
    return {ii[0]:ii[1] for ii in tp}

def get_pos(sites):
    lons=[]
    lats=[]
    pos=get_pos_dic()
    for site in sites:
        tp=pos[site]
        lons.append(tp[0])
        lats.append(tp[1])
    return lons,lats

class MapPlotDisplacement(MapPlot):
    def __init__(self,
                 basemap=None):
        super().__init__(basemap=basemap)
    
    def plot_disp(self,d,sites,
                  X=0.1,Y=0.1,U=1.,label='1m',
                  color='black',scale=None):
        ''' Plot displacment
'''
            
        lons,lats=get_pos(sites)
        es=d[0::3]
        ns=d[1::3]
        us=d[2::3]
        Qu = self.basemap.quiver(lons,lats,es,ns,
                    color=color,scale=scale,edgecolor=color,latlon=True)
        qk = quiverkey(Qu,X,Y,U,label,
                            labelpos='N')

    def plot_sites(self, sites,
                   marker='s', color='white', ms=5):
        lons,lats=get_pos(sites)
        self.basemap.plot(lons,lats, linestyle='None', 
                          marker=marker, color=color, ms=ms, latlon=True)

    def plot_sites_seafloor(self, sites_file=None, sites_seafloor=None):
        if sites_file is None:
            sites_seafloor = vj.read_sites_seafloor(
                join(this_file_path, 'share/sites_with_seafloor'))
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
        
        
        
        
    
