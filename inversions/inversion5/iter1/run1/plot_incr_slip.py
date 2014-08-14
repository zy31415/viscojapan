from pylab import show, savefig, close
import glob
from os.path import join, exists, basename
from os import makedirs
from multiprocessing import Pool
import sys

import h5py
from numpy import loadtxt

import viscojapan as vj
from viscojapan.plots import MapPlotFault, MapPlotSlab, plt
from viscojapan.fault_model import FaultFileIO

sys.path.append('..')
from epochs_log import epochs
from alphas import alphas


fault_file = '../fault_model/fault_bott40km.h5'

fid = FaultFileIO(fault_file)
num_subflts = fid.num_subflt_along_strike*fid.num_subflt_along_dip

sites = loadtxt('../sites_with_seafloor','4a,')
num_obs = len(sites)*3

d_ep = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5')

scale = 20

def task(f_res):
    print(f_res)
    file = basename(f_res)
    plot_dir = join('plots', file.split('.')[0])
    if not exists(plot_dir):
        makedirs(plot_dir)
        
    with h5py.File(f_res) as fid:
        Bm = fid['Bm'][...]
        d_pred = fid['d_pred'][...]

    for nth, epoch in enumerate(epochs):    
        mplt = MapPlotFault(fault_file)
        mplt.plot_slip(Bm[nth*num_subflts:
                          (nth+1)*num_subflts])

        mplt = vj.MapPlotDisplacement()
        mplt.plot_disp(d_pred[nth*num_obs:
                              (nth+1)*num_obs],sites, scale=scale)

        mplt.plot_disp(d_ep[epoch],d_ep.sites, color='red', scale=scale)
        
        mplt = MapPlotSlab()
        mplt.plot_top()
        
        savefig(join(plot_dir, 'incr_slip_%04d.png'%epoch))
        # plt.show()
        plt.close()

if __name__ == '__main__':
    nproc = 22
    pool = Pool(processes=nproc)
    files = glob.glob('outs/ano_??_bno_??_nsd_00.h5')
    pool.map(task, files)
