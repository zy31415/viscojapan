import sqlite3

import numpy as np

import viscojapan as vj

result_file = '../../outs/nrough_05_naslip_11.h5'

pred = vj.inv.DeformPartitionerForResultFile(
    result_file = result_file,
    file_G0 = '../../../green_function_large_scale/G0_He50km_VisM6.3E18_Rake83.h5',
    files_Gs = ['../../../green_function_large_scale/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function_large_scale/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function_large_scale/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    file_slip0 = '../../slip0/slip0.h5',
    )

pred.save('partition_large_scale.h5')


