from pylab import show, savefig, close
import glob

import h5py

from viscojapan.plots import MapPlotFault, MapPlotSlab, plt
from viscojapan.fault_model import FaultFileIO

from epochs_log import epochs

ano = 8
bno = 7


file = glob.glob('../../outs/ano_%02d_bno_%02d.h5'%(ano,bno))[0]
fault_file = '../../../../../fault_model/fault_He50km_east.h5'

fid = FaultFileIO(fault_file)
num_subflts = fid.num_subflt_along_strike*fid.num_subflt_along_dip

with h5py.File(file) as fid:
    Bm = fid['Bm'][...]

for nth, epoch in enumerate(epochs):    
    print(epoch)
    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(Bm[nth*num_subflts:
                      (nth+1)*num_subflts])
    mplt = MapPlotSlab()
    mplt.plot_top()
    
    savefig('plots/incr_slip_%04d.png'%epoch)
    plt.show()
    plt.close()
