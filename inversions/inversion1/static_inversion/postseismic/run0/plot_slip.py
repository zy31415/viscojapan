import glob
from os.path import basename, exists
import re
from multiprocessing import Pool
import argparse

import h5py

from viscojapan.plots import MapPlotFault, plt, MapPlotSlab
import viscojapan as vj


files = glob.glob('outs/nsd_??_rough_10_top_02.h5')

sites_seafloor = vj.get_sites_seafloor()

def plot_file(file):
    name = basename(file)
    fname = 'plots/%s.pdf'%name
    if exists(fname):
        print('Skip %s!'%fname)
        return
    print(fname)
    with h5py.File(file,'r') as fid:
        slip = nres = fid['Bm'][...]

    mplt = MapPlotSlab()
    mplt.plot_top()
    
    mplt = MapPlotFault('../fault_bott40km.h5')
    mplt.plot_slip(slip)

    mplt = vj.MapPlotDisplacement()
    mplt.plot_sites_seafloor(sites_seafloor = sites_seafloor)
    #plt.show()
    plt.savefig(fname)

    plt.close()

for file in files:
    plot_file(file)

    
