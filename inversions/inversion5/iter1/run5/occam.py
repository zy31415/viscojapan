from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import \
     create_temporal_edge_roughening
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs
from reg_edges import reg_edges
from reg_roughes import reg_roughes

print(reg_edges)
print(reg_roughes)

fault_file = '../fault_model/fault_bott40km.h5'

basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = '../green_function/G_He40km_Vis5.8E18_Rake81.h5',
    
    files_Gs = ['../green_function/G_He40km_Vis1.1E19_Rake81.h5',
                '../green_function/G_He45km_Vis5.8E18_Rake81.h5',
                '../green_function/G_He40km_Vis5.8E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','He','rake'],

    file_d = '../../cumu_post_with_seafloor.h5',
    file_sd = '../../sd_seafloor/sd_files/sd_with_seafloor_03.h5', 
    file_incr_slip0 = '../slip0/incr_slip0.h5',
    filter_sites_file = '../sites_with_seafloor',
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

        
            
