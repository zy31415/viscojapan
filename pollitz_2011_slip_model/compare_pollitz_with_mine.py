import numpy as np
from pylab import plt

import pyproj
import h5py

import viscojapan as vj

def compute_moment(lons,lats,slip):
    # compute mo
    g = pyproj.Geod(ellps='WGS84')
    az1, az2, dist = g.inv(lons[0,0:-1], lats[0,0:-1],
                           lons[0,1:], lats[0,1:])
    dx = dist.mean()
    az1, az2, dist = g.inv(lons[0:-1,0], lats[0:-1,0],
                           lons[1:, 0], lats[1:,0])
    dy = dist.mean()
    Mo = dx*dy*slip.sum()*40e9

    Mw = 2/3*np.log10(Mo) - 6.

    return Mo, Mw

tp = np.loadtxt('Pollitz-slipmodel.txt')

lons = tp[:,0].reshape([42,-1])
lats = tp[:,1].reshape([42,-1])
slip = tp[:,3].reshape([42,-1])

plt.subplot(121)
bm = vj.MyBasemap()
bm.pcolor(lons,lats,slip,latlon=True)
bm.colorbar()
mplt = vj.MapPlotSlab()
mplt.plot_top()

Mo, Mw = compute_moment(lons,lats,slip)
plt.title('Mo=%g, Mw=%.2f'%(Mo,Mw))

plt.subplot(122)
bm = vj.MyBasemap()

bm.colorbar()
mplt = vj.MapPlotSlab()
mplt.plot_top()
with h5py.File('../inversions/static_inversion/coseismic/run0/outs/ndamp_00_rough_09.h5','r') as fid:
    slip = nres = fid['Bm'][...]

fault_file = '../inversions/static_inversion/fault_model/fault_bott50km.h5'
with h5py.File(fault_file,'r') as fid:
    lons = fid['meshes/LLons'][...]
    lats = fid['meshes/LLats'][...]

bm.pcolor(lons[1:,1:],lats[1:,1:],slip.reshape([11,35]),latlon=True)

Mo, Mw = compute_moment(lons,lats,slip)
plt.title('Mo=%g, Mw=%.2f'%(Mo,Mw))
plt.show()

