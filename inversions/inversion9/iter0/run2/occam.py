from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.basis_function import BasisMatrix

from epochs import epochs
from reg_roughes import reg_roughes

fault_file = '../fault_model/fault_bott60km.h5'

basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = '../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    
    files_Gs = ['../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../green_function/G2_He40km_VisM6.3E18_Rake83.h5',
                '../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','log10(He)','rake'],

    file_d = '../obs/cumu_post_with_seafloor.h5',
    file_sd = 'sd/sd_uniform_seafloor_inf.h5', 
    file_incr_slip0 = 'slip0/slip0.h5',
    filter_sites_file = 'sites_2EXPs',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )

inv.set_data_except(excepts=['L'])

reg_boundary = 0.06
regs_co = logspace(-3,1,20)
regs_aslip = logspace(-3,1,20)

for nco, reg_co in enumerate(regs_co):
    for naslip, reg_aslip in enumerate(regs_aslip):
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

        
            
