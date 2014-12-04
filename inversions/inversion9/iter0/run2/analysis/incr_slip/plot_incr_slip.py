import glob
from os.path import join, exists
from os import makedirs

from pylab import show, savefig, close
import h5py

from viscojapan.plots import MapPlotFault, MapPlotSlab, plt
import viscojapan as vj

from epochs import epochs

outfile = '../../outs/nco_06_naslip_13.h5'

fault_file = '../../../fault_model/fault_bott60km.h5'

reader = vj.inv.ResultFileReader(outfile)

for epoch in epochs:
    slip = reader.get_incr_slip_at_epoch(epoch)

    plot_path = 'incr_slip/'
    if not exists(plot_path):
        makedirs(plot_path)

    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(slip)

    mplt = MapPlotSlab()
    mplt.plot_top()
    
    savefig(join(plot_path, 'incr_slip_%04d.png'%epoch))
    plt.show()
    plt.close()
    
