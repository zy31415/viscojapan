import sqlite3

import numpy as np

import viscojapan as vj

slip_file = '../slip_extrapolation/extra_slip_EXP.h5'
slip = vj.epoch_3d_array.Slip.load(slip_file)
epochs = slip.get_epochs()

result_file = '../../outs/nrough_06_naslip_11.h5'
result_file_reader = vj.inv.ResultFileReader(result_file)

pred = vj.inv.DeformPartitioner(
    epochs = epochs,
    slip = slip,
    nlin_pars = result_file_reader.nlin_par_solved_values,
    nlin_par_names = result_file_reader.nlin_par_names,
    file_G0 = '../../../green_function_large_scale/G0_He50km_VisM6.3E18_Rake83.h5',
    files_Gs = ['../../../green_function_large_scale/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function_large_scale/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function_large_scale/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    file_slip0 = '../../slip0/slip0.h5',
    )

pred.save('deformation_partition_large_scale.h5')


