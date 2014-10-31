from numpy import logspace
import numpy as np

import viscojapan as vj
from viscojapan.inversion.basis_function import BasisMatrix, BasisMatrixBSpline
from viscojapan.inversion.regularization import Roughening, Composite, \
     NorthBoundary, SouthBoundary, FaultTopBoundary
from viscojapan.inversion.static_inversion import StaticInversion


fault_file = '../../fault_model/fault_bott60km.h5'

rough = Roughening.create_from_fault_file(fault_file)
damping = vj.Intensity.create_from_fault_file(fault_file)
reg_north = NorthBoundary.create_from_fault_file(fault_file)
reg_south = SouthBoundary.create_from_fault_file(fault_file)
reg_top = FaultTopBoundary.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)
basis_b_spline = BasisMatrixBSpline.create_from_fault_file(fault_file)

inv = StaticInversion(
    file_G = '../../green_function/G5_He63km_VisM1.0E19_Rake83.h5',
    file_d = '../../cumu_post_with_seafloor.h5',
    file_sd = '../sd/sd_seafloor_inf.h5',
    file_sites_filter = 'sites_with_seafloor',
    regularization = None,
    basis = basis,
)
inv.set_data_except(excepts=['L'])

roughs = logspace(-4, 0, 30)
for nrough in range(len(roughs)):
    outf = 'outs/rough_%02d.h5'%(nrough)
    print(outf)
    reg = Composite().add_component(component = rough,
                                    arg = roughs[nrough],
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    
    inv.save(outf, overwrite=True)
