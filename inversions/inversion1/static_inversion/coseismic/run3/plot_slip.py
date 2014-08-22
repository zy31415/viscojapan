import glob
from os.path import basename, exists
import re
from multiprocessing import Pool

import h5py

from viscojapan.plots import MapPlotFault, plt, MapPlotSlab
import viscojapan as vj

files = glob.glob('outs/rough_??_top_??.h5')

sites_seafloor = vj.read_sites_seafloor('../sites_with_seafloor')

def plot_file(file):
    name = basename(file)
    fname = 'plots/%s.png'%name
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

if __name__=='__main__':        
    nproc = 5
    pool = Pool(5)   
    pool.map(plot_file, files)

    
