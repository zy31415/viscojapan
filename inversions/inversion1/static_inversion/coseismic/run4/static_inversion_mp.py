from numpy import logspace
import numpy as np
from multiprocessing import Pool
import argparse
import sys
import os

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite, \
     NorthBoundary, SouthBoundary, FaultTopBoundary
from viscojapan.inversion.static_inversion import StaticInversion

parser = argparse.ArgumentParser(description='Plot slip.')
parser.add_argument('ncpus', type=int, nargs=1, help='# CPUs')
args = parser.parse_args()

ncpus = args.ncpus[0]

fault_file = '../fault_bott40km.h5'

rough = Roughening.create_from_fault_file(fault_file)
reg_north = NorthBoundary.create_from_fault_file(fault_file)
reg_south = SouthBoundary.create_from_fault_file(fault_file)
reg_top = FaultTopBoundary.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)


inv = StaticInversion(
    file_G = '../G_He40km_Vis1.1E19_Rake81.h5',
    file_d = '../cumu_post_with_seafloor.h5',
    file_sd = None,
    file_sites_filter = '../sites_with_seafloor',
    regularization = None,
    basis = basis,
)
inv.set_data_except(excepts=['L','sd','W'])

roughs = logspace(-3, 1, 30)
edge_pars = np.logspace(-3,1,10)

def run(par):
    nsd = par[0]
    nrough = par[1]
    nedg = par[2]
    outf = 'outs/nsd_%02d_rough_%02d_top_%02d.h5'%(nsd, nrough, nedg)
    print(outf)
    stdout = sys.stdout
    sys.stdout = os.devnull

    reg = Composite().\
          add_component(component = reg_north,
                        arg = 1e5,
                        arg_name = 'north').\
          add_component(component = reg_south,
                        arg = 1e5,
                        arg_name = 'south').\
          add_component(component = rough,
                        arg = roughs[nrough],
                        arg_name = 'roughening').\
          add_component(component = reg_top,
                        arg = edge_pars[nedg],
                        arg_name = 'top')
    
    inv.regularization = reg
    inv.file_sd = '../sd_seafloor/sd_files/sd_with_seafloor_%02d.h5'%nsd
    inv.set_data_L()
    inv.set_data_sd()
    inv.set_data_W()
    inv.invert()
    inv.predict()
    
    inv.save(outf, overwrite=True)

    sys.stdout = stdout

if __name__=='__main__':
    pars = []
    for nsdi in range(10):
        for nroughi in range(len(roughs)):
            for nedgi in range(len(edge_pars)):
                pars.append([nsdi, nroughi, nedgi])
    pool = Pool(ncpus)
    pool.map(run, pars)
