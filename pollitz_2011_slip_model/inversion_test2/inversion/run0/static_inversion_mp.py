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

roughs = logspace(-3, 1, 30)
def run(epoch):
    print(epoch)
    stdout = sys.stdout
    fid = open(os.devnull,'w')
    sys.stdout = fid
    
    inv = StaticInversion(
        file_G = '../G_He40km_Vis1.1E19_Rake81.h5',
        file_d = '../cumu_post_with_seafloor.h5',
        file_sd = '../sd/sd_ozawa.h5',
        file_sites_filter = '../sites_with_seafloor',
        regularization = None,
        basis = basis,
        epoch = epoch,
    )
    inv.set_data_except(excepts=['L'])
    for nrough in range(len(roughs)):
        outf = 'outs/epoch_%04d_rough_%02d.h5'%(epoch,nrough)
        print(outf)
        
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
                            arg = 0.02,
                            arg_name = 'top')
        
        inv.regularization = reg
        inv.set_data_L()
        inv.invert()
        inv.predict()
        
        inv.save(outf, overwrite=True)

    sys.stdout = stdout
    fid.close()

if __name__=='__main__':
    from epochs import epochs
    pool = Pool(ncpus)
    pool.map(run, epochs)
