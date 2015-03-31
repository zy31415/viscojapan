from numpy import logspace
import numpy as np

from os.path import exists
import sys

import viscojapan as vj

from epochs import epochs_list

reg_roughes = logspace(-3,1,20)

fault_file = '../fault_model/fault_bott80km.h5'

sites = np.loadtxt('sites_with_seafloor', '4a', usecols=(0,))
sites = vj.utils.as_string(sites)

reg_boundary = 0.06
regs_rough = logspace(-3,1,20)
regs_aslip = logspace(-3,1,20)

for nrough, reg_rough, naslip, reg_aslip in \
        vj.utils.pop_from_center((6,11), regs_rough, regs_aslip):

    for nth_epochs, epochs in enumerate(epochs_list):
        epochs = epochs[0:3]
        num_epochs = len(epochs)

        # unit basis matrix
        basis = vj.inv.basis.BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))
        
        inv = vj.inv.OccamDeconvolution(
            file_G0 = '../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
            files_Gs = ['../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                        '../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                        '../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                        ],
            nlin_par_names = ['log10(visM)','log10(He)','rake'],

            file_d = '../obs/cumu_post_with_seafloor.h5',
            file_sd = 'sd/sd_uniform.h5', 
            file_slip0 = 'slip0/slip0.h5',
            sites = sites,
            epochs = epochs,
            regularization = None,
            basis = basis,
            decreasing_slip_rate=True
            )

        inv.set_data_except(excepts=['L'])
        
        outfname = 'outs/nepochs_%02d_nrough_%02d_naslip_%02d.h5'%\
                   (nth_epochs, nrough, naslip)
        if exists(outfname):
            print("Skip %s !"%outfname)
            continue
        print(outfname)
        inv.regularization = \
               reg = vj.inv.reg.create_rough_aslip_boundary_regularization(
                   fault_file, num_epochs,
                   reg_rough,
                   reg_aslip,
                   reg_boundary)
        
        inv.set_data_L()
        inv.run()
        inv.save(outfname, overwrite=True)
                
                        
