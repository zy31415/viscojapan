import h5py
import glob
import os

import viscojapan as vj
from viscojapan.plots import MapPlotFault, plt

files = sorted(glob.glob('outs/dip3_stk4_ano_??.h5'))

for file in files:
    f1 = os.path.basename(file)
    with h5py.File(file ,'r') as fid:
        slip = nres = fid['Bm'][...]
        mplt = MapPlotFault('../../fault_model/fault_bott80km.h5')
        mplt.plot_slip(slip, zorder=-2,
                       cb_shrink=0.7,
                       cb_pad = 0.1)

        mplt = vj.plots.MapPlotSlab()
        mplt.plot_top()
        
        
        plt.clim([0,2])
        #plt.show()
        
        plt.savefig(
            os.path.join('plots',f1.split('.')[0]+'.png')
            )

        plt.savefig(
            os.path.join('plots',f1.split('.')[0]+'.pdf')
            )
        
        plt.close()
