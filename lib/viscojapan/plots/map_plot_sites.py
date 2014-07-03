from os.path import join
from numpy import loadtxt
from pylab import quiverkey

from .my_basemap import MyBasemap

from ..utils import get_this_script_dir
from ..epochal_data import EpochalDisplacement

this_file_path = get_this_script_dir(__file__)

def get_pos_dic():
    ''' Return a dictionary of position of all stations.
'''
    tp=loadtxt(join(this_file_path, 'sites_with_seafloor'),'4a, 2f')
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

class MapPlotDisplacement(MyBasemap):
    def __init__(self):
        super().__init__()
    
    def plot_disp(self,d,sites,
                  X=0.1,Y=0.1,U=1.,label='1m',
                  color='black',scale=None):
        ''' Plot displacment
'''
        if not self.if_init:
            self.init()
            
        lons,lats=get_pos(sites)
        es=d[0::3]
        ns=d[1::3]
        us=d[2::3]
        Qu = self.quiver(lons,lats,es,ns,
                    color=color,scale=scale,edgecolor=color,latlon=True)
        qk = quiverkey(Qu,X,Y,U,label,
                            labelpos='N')

    def plot_disp_file(self, f_disp, epoch):
        disp_obj = EpochalDisplacement(f_disp)
        disp = disp_obj(epoch)
        sites = disp_obj.get_info('sites')
        self.plot_disp(disp, sites)
        
    
