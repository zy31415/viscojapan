import glob
from os.path import basename, exists
import re
from multiprocessing import Pool
import argparse

import h5py

from viscojapan.plots import MapPlotFault, plt, MapPlotSlab
import viscojapan as vj


parser = argparse.ArgumentParser(description='Plot slip.')
parser.add_argument('ncpus', type=int, nargs=1, help='# CPUs')
args = parser.parse_args()

ncpus = args.ncpus[0]

files = glob.glob('outs/nrough_??_ntop_??.h5')

fault_file = '../../fault_model/fault_bott60km.h5'
earth_file = '../../earth_model_nongravity/He63km_VisM1.0E19/earth.model_He63km_VisM1.0E19'
#sites_seafloor = vj.read_sites_seafloor('../sites_with_seafloor')

def plot_file(file):
    name = basename(file)
    fname = 'plots/pdf/%s.pdf'%name.split('.')[0]
    if exists(fname):
        print('Skip %s!'%fname)
        return
    print(fname)
    with h5py.File(file,'r') as fid:
        slip = nres = fid['Bm'][...]

    mplt = MapPlotSlab()
    mplt.plot_top()
    
    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(slip)

    mplt = vj.plots.MapPlotDisplacement()
    mplt.plot_sites_seafloor(text=False)

    mo, mw = vj.ComputeMoment(fault_file, earth_file).moment(slip)
    plt.title('Mo=%g, Mw=%.2f'%(mo, mw))
    
    #plt.show()
    plt.savefig(fname)

    plt.close()

if __name__=='__main__':
    pool = Pool(ncpus)   
    pool.map(plot_file, files)

    
