from numpy import logspace
import numpy as np
from multiprocessing import Pool
import argparse
import sys
import os

from viscojapan.inversion.basis_function import BasisMatrix, BasisMatrixBSpline
from viscojapan.inversion.regularization import Roughening, Composite, \
     NorthBoundary, SouthBoundary, FaultTopBoundary
from viscojapan.inversion.static_inversion import StaticInversion

parser = argparse.ArgumentParser(description='Plot slip.')
parser.add_argument('ncpus', type=int, nargs=1, help='# CPUs')
args = parser.parse_args()

ncpus = args.ncpus[0]

fault_file = '../../fault_model/fault_bott60km.h5'

rough = Roughening.create_from_fault_file(fault_file)
reg_north = NorthBoundary.create_from_fault_file(fault_file)
reg_south = SouthBoundary.create_from_fault_file(fault_file)
reg_top = FaultTopBoundary.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)
basis_b_spline = BasisMatrixBSpline.create_from_fault_file(fault_file)

reg_roughs = logspace(-4, 0, 30)
reg_tops = logspace(-4, 0, 10)

def run(nregs):
    nrough = nregs[0]
    ntop = nregs[1]
    outf = 'outs/nrough_%02d_ntop_%02d.h5'%(nrough, ntop)
    print(outf)
    stdout = sys.stdout
    fid = open(os.devnull,'w')
    sys.stdout = fid
    
    inv = StaticInversion(
        file_G = '../../green_function/G5_He63km_VisM1.0E19_Rake83.h5',
        file_d = '../../cumu_post_with_seafloor.h5',
        file_sd = '../sd/sd_seafloor_02.h5',
        file_sites_filter = 'sites_with_seafloor',
        regularization = None,
        basis = basis_b_spline,
    )
    inv.set_data_except(excepts=['L'])

    
    
    reg = Composite().\
          add_component(component = reg_north,
                        arg = 1e5,
                        arg_name = 'north').\
          add_component(component = reg_south,
                        arg = 1e5,
                        arg_name = 'south').\
          add_component(component = rough,
                        arg = reg_roughs[nrough],
                        arg_name = 'roughening').\
          add_component(component = reg_top,
                        arg = reg_tops[ntop],
                        arg_name = 'top')
        
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    
    inv.save(outf, overwrite=True)

    sys.stdout = stdout
    fid.close()

if __name__=='__main__':
    pool = Pool(ncpus)

    nregs = [(ii, jj) for ii in range(len(reg_roughs))
             for jj in range(len(reg_tops))]
    
    pool.map(run, nregs)
