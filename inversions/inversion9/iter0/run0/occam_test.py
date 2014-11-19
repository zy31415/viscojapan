from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import \
     create_temporal_edge_roughening
from viscojapan.inversion.basis_function import BasisMatrix

from epochs import epochs
from reg_edges import reg_edges
from reg_roughes import reg_roughes

fault_file = '../fault_model/fault_bott60km.h5'

epochs = epochs[0:4]

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
    file_incr_slip0 = 'slip0/incr_slip0_patched.h5',
    filter_sites_file = 'sites_2EXPs',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )

inv.set_data_except(excepts=['L'])

reg_temp = 0
reg_edge = 0.06
for nrough, reg_rough in enumerate(reg_roughes):
    outfname = 'outs/nrough_%02d.h5'%(nrough)
    if exists(outfname):
        print("Skip %s !"%outfname)
        continue
    print(outfname)
    inv.regularization = \
           reg = vj.create_temporal_edge_roughening(
               fault_file, epochs, reg_temp, reg_edge, reg_rough)
    
    inv.set_data_L()
    inv.run()
    inv.save(outfname, overwrite=True)

        
            
