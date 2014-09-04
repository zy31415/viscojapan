from pylab import show, savefig, close
import glob
from os.path import join, exists, basename
from os import makedirs
from multiprocessing import Pool
import sys

import h5py
from numpy import loadtxt, amax

import viscojapan as vj
from viscojapan.plots import MapPlotFault, MapPlotSlab, plt, MyBasemap
from viscojapan.fault_model import FaultFileIO

sys.path.append('../../')
from epochs_log import epochs
from alphas import alphas


fault_file = '../../fault_model/fault_bott40km.h5'

fid = FaultFileIO(fault_file)
num_subflts = fid.num_subflt_along_strike*fid.num_subflt_along_dip

sites = loadtxt('../../sites_with_seafloor','4a,')
num_obs = len(sites)*3


f_res = '../outs/seasd_01_nrough_10_nedge_05.h5'

file = basename(f_res)
plot_dir = 'plots/'

with h5py.File(f_res,'r') as fid:
    Bm = fid['Bm'][...]

for nth, epoch in enumerate(epochs):
    print(epoch)
    fname = join(plot_dir, 'incr_slip_%04d.pdf'%epoch)
    bm = MyBasemap(region_code='near')
    scale = 10
    mplt = MapPlotFault(fault_file,bm)
    if epoch==0:
        clim = [0,amax(Bm[:-3])]
    else:
        clim = [0,amax(Bm[num_subflts:-3])]
        
    mplt.plot_slip(Bm[nth*num_subflts:
                      (nth+1)*num_subflts],clim=clim)
    
    mplt = MapPlotSlab(bm)
    mplt.plot_top()
    
    savefig(fname)
    #plt.show()
    plt.close()

