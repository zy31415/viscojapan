from pylab import show, savefig, close
import glob
from os.path import join, exists
from os import makedirs
import os

import h5py
from numpy import loadtxt

import viscojapan as vj
from viscojapan.plots import MapPlotFault, MapPlotSlab, plt
from viscojapan.fault_model import FaultFileIO

from epochs import epochs


fault_file = '../fault_model/fault_bott50km.h5'

fid = FaultFileIO(fault_file)
num_subflts = fid.num_subflt_along_strike*fid.num_subflt_along_dip

sites = loadtxt('sites','4a,')
num_obs = len(sites)*3

files = glob.glob('outs/nrough_??.h5')

scale = 20

for file in files:    
    print(file)
    bn = os.path.basename(file).split('.')[0]
    plot_dir = 'plots/%s'%bn
    if not exists(plot_dir):
        makedirs(plot_dir)
    
    with h5py.File(file) as fid:
        Bm = fid['Bm'][...]
        d_pred = fid['d_pred'][...]

    for nth, epoch in enumerate(epochs[1:]):    
        print(epoch)
        mplt = MapPlotFault(fault_file)
        mplt.plot_slip(Bm[nth*num_subflts:
                          (nth+1)*num_subflts])

##        mplt = vj.MapPlotDisplacement()
##        mplt.plot_disp(d_pred[nth*num_obs:
##                              (nth+1)*num_obs],sites, scale=scale)
##        sites = [ii.decode() for ii in d_ep.sites]
##        mplt.plot_disp(d_ep[epoch], sites, color='red', scale=scale)
        
        mplt = MapPlotSlab()
        mplt.plot_top()
        
        savefig(join(plot_dir, 'incr_slip_%04d.png'%epoch))
        # plt.show()
        plt.close()
