import glob
from os.path import basename, exists

import h5py

from viscojapan.plots import MapPlotFault, plt

files = glob.glob('outs/ano_??_edg_??.h5')

for ano in range(30):
    for file in files:
        name = basename(file)
        fname = 'plots/%s.png'%name
        if exists(fname):
            print('Skip %s!'%fname)
            continue
        print(fname)
        with h5py.File(file,'r') as fid:
            slip = nres = fid['Bm'][...]
        mplt = MapPlotFault('fault_bott40km.h5')
        mplt.plot_slip(slip)
        #plt.show()
        plt.savefig(fname)
        plt.close()
