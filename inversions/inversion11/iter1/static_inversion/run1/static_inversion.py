from os.path import join, exists
from os import makedirs

from numpy import logspace
import numpy as np

import viscojapan as vj
from viscojapan.inversion.basis_function import BasisMatrix, BasisMatrixBSpline
from viscojapan.inversion.static_inversion import StaticInversion

from epochs import epochs

fault_file = '../../fault_model/fault_bott80km.h5'

rough = vj.inv.reg.Roughening.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)
basis_b_spline = BasisMatrixBSpline.create_from_fault_file(fault_file)

reg_roughes = logspace(-3,1,20)

for epoch in epochs:
    inv = StaticInversion(
        file_G = '../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
        file_d = '../../obs/cumu_post_with_seafloor.h5',
        file_sd = 'sd/sd_uniform.h5',
        filter_sites_file = 'sites_with_seafloor',
        regularization = None,
        basis = basis,
        fault_file=fault_file,
        epoch = epoch,
    )
    inv.set_data_except(excepts=['L']) 
    
    for nrough, r in enumerate(reg_roughes):
        outf_dir = 'outs/outs_%04d/'%epoch
        if not exists(outf_dir):
            makedirs(outf_dir)
        outf = join(outf_dir, 'rough_%02d.h5'%(nrough))
        print(outf)
        reg = vj.inv.reg.Composite().add_component(component = rough,
                                        arg = r,
                                        arg_name = 'roughening')
        inv.regularization = reg
        inv.set_data_L()
        inv.invert()
        inv.predict()
        
        inv.save(outf, overwrite=True)
