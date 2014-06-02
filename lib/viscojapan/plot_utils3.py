#!/usr/bin/env python3
from pylab import *
from mpl_toolkits.basemap import Basemap
from h5py import File

def get_pos_dic():
    ''' Return a dictionary of position of all stations.
'''
    tp=loadtxt('/home/zy/workspace/utils/llh','4a,3f')
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

_fault_file='/home/zy/workspace/greens/faults/fault_60km.h5'

def moment(slip):
    ''' Compute moment.
'''
    with File(_fault_file) as fid:
        fl=float(fid['subflt_len_stk'][...])
        fw=float(fid['subflt_wid_dip'][...])
        shr=fid['meshes/shear'][...][1:,1:]
    mos=shr.flatten()*slip.flatten()*fl*1e3*fw*1e3
    mo=sum(mos)
    mw=2./3.*log10(mo)-6. 
    return mo, mw

class Map(Basemap):
    def __init__(self):
        self.region_box=(136,34,146,42)
        self.region_code=None
        self.x_interval=2.
        self.y_interval=2.

    def init(self):
        if self.region_code is not None:
            if self.region_code=='I':
                self.region_box=(128,30,132.5,34.5)
            elif self.region_code=='A':
                self.region_box=(136.2,35.8,142.6,38.2)
            elif self.region_code=='H':
                self.region_box=(131,33,137,36.5)
            elif self.region_code=='E':
                self.region_box=(140,41.8,146.2,45.8)
            elif self.region_code=='near':
                self.region_box=(136,34,146,42)
            else:
                raise ValueError()
        
                
        self.lon_0=(self.region_box[0]+self.region_box[2])/2.
        self.lat_0=(self.region_box[1]+self.region_box[3])/2.
        super().__init__(llcrnrlon=self.region_box[0],llcrnrlat=self.region_box[1],
                         urcrnrlon=self.region_box[2],urcrnrlat=self.region_box[3],
                         resolution='l',area_thresh=100.,projection='eqdc',
                         lon_0=self.lon_0,lat_0=self.lat_0,
                         lat_1=self.lat_0-5,lat_2=self.lat_0+5)

        self.drawcoastlines(color='green',zorder=-1)

        # draw parallels and meridians.
        self.drawparallels(arange(-80.,81.,self.y_interval),zorder=-1,labels=[1,1,0,0])
        self.drawmeridians(arange(-180.,181.,self.x_interval),zorder=-1,labels=[0,0,0,1])
        self.drawmapboundary(color='k')

        return self

    def plot_disp(self,d,sites,
                  X=0.1,Y=0.1,U=1.,label='1m',
                  color='black',scale=None):
        ''' Plot displacment
'''
        lons,lats=get_pos(sites)
        xpt,ypt=self(lons,lats)
        es=d[0::3]
        ns=d[1::3]
        us=d[2::3]
        Qu=self.quiver(xpt,ypt,es,ns,
                    color=color,scale=scale,edgecolor=color)
        qk=quiverkey(Qu,X,Y,U,label,
                            labelpos='N')

    def plot_fslip(self,m,cmap=None,clim=None):
        '''
'''
        with File('/home/zy/workspace/greens/faults/fault_60km.h5') as fid:
            LLons=fid['meshes/LLons'][...][1:,1:]
            LLats=fid['meshes/LLats'][...][1:,1:]
            
        mm=m.reshape([-1,40])
        xpt,ypt=self(LLons,LLats)
        self.pcolor(xpt,ypt,mm,zorder=-1,cmap=cmap)
        cb=colorbar()
        plt.clim(clim)
        cb.set_label('disp.(m)')
        mo,mw=moment(m)
        title('Mo=%.3g,Mw=%.2f'%(mo,mw))
        

    def plot_fault(self,fno,ms=15):
        with File('/home/zy/workspace/greens/faults/fault_60km.h5') as fid:
            LLons=fid['meshes/LLons'][...][1:,1:]
            LLats=fid['meshes/LLats'][...][1:,1:]

        xpt,ypt=self(LLons,LLats)        
        self.plot(xpt,ypt,color='gray')
        self.plot(xpt.T,ypt.T,color='gray')
        self.plot(xpt.flatten()[fno],ypt.flatten()[fno],
             marker='*',color='red',ms=ms)
        
        

    
