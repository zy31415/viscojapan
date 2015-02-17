import sqlite3

import numpy as np

import viscojapan as vj

result_file = '../../outs/nrough_05_naslip_11.h5'

pred = vj.inv.DeformPartitionerForResultFile(
    file_G0 = '../../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    result_file = result_file,
    files_Gs = ['../../../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    file_slip0 = '../../slip0/slip0.h5',
    #sites_for_prediction = ['J550'],
    )

pred.save('deformation_partition.h5')


    
