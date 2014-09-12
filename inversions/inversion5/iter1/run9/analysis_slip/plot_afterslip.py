from pylab import show, savefig, close
import glob
from os.path import join, exists, basename
import sys

import h5py
from numpy import loadtxt, amax, zeros_like

import viscojapan as vj
from viscojapan.plots import MapPlotFault, MapPlotSlab, plt, MyBasemap
from viscojapan.fault_model import FaultFileIO

sys.path.append('../../')
from epochs_log import epochs
from alphas import alphas


fault_file = '../../fault_model/fault_bott40km.h5'

fid = FaultFileIO(fault_file)
num_subflt_along_dip = fid.num_subflt_along_dip
num_subflt_along_strike = fid.num_subflt_along_strike
num_subflts = num_subflt_along_strike * num_subflt_along_dip

sites = loadtxt('../../sites_with_seafloor','4a,')
num_obs = len(sites)*3

num_epochs = len(epochs)

f_res = '../outs/seasd_01_nrough_10_nedge_05.h5'

plot_dir = 'plots/'

with h5py.File(f_res,'r') as fid:
    Bm = fid['Bm'][...]
slip = Bm[:-3].reshape([num_epochs,
                        num_subflt_along_dip, num_subflt_along_strike])

afterslip = zeros_like(slip[1,:,:])
for s, epoch in zip(slip[1:,:,:],epochs[1:]):
    print(epoch)

    afterslip += s
    fname = join(plot_dir, 'afterslip_%04d.pdf'%epoch)

    mplt = MapPlotSlab()
    mplt.plot_top()

    bm = MyBasemap(region_code='near')
    mplt = MapPlotFault(fault_file)
    clim = [0,24]    
    mplt.plot_slip(afterslip.reshape([-1,1]),clim=clim)
    
    savefig(fname)
    #plt.show()
    plt.close()

