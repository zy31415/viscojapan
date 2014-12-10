from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.basis_function import BasisMatrix

from epochs import epochs

fault_file = '../fault_model/fault_bott120km.h5'

epochs = epochs[0:3]
num_epochs = len(epochs)

basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = '../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    files_Gs = ['../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                '../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','log10(He)','rake'],

    file_d = '../obs/cumu_post_with_seafloor.h5',
    file_sd = '../sd/sd_uniform.h5', 
    file_incr_slip0 = 'slip0/slip0.h5',
    filter_sites_file = 'sites_with_seafloor',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )

inv.set_data_except(excepts=['L'])

reg_boundary = 0.06
regs_co = logspace(-3,1,20)
regs_aslip = logspace(-3,1,20)


for naslip, reg_aslip in enumerate(regs_aslip):
    for nco, reg_co in enumerate(regs_co):    
        outfname = 'outs/nco_%02d_naslip_%02d.h5'%(nco, naslip)
        if exists(outfname):
            print("Skip %s !"%outfname)
            continue
        print(outfname)
        inv.regularization = \
               reg = vj.inv.reg.create_co_aslip_boundary_regularization(
                   fault_file, num_epochs,
                   reg_co, reg_aslip, reg_boundary)
        
        inv.set_data_L()
        inv.run()
        inv.save(outfname, overwrite=True)

        
            
