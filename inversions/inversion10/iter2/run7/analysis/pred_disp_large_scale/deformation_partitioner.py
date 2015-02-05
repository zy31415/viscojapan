import sqlite3

import numpy as np

import viscojapan as vj

result_file = '../../outs/nrough_05_naslip_11.h5'
fault_file = '../../../fault_model/fault_bott80km.h5'

res_reader = vj.inv.ResultFileReader(result_file)

slip = res_reader.get_slip(fault_file)

pred = vj.inv.DeformPartitioner2Disp(
    file_G0 = '../../../green_function_large_scale/G0_He50km_VisM6.3E18_Rake83.h5',
    slip = slip,
    epochs = slip.epochs,
    files_Gs = ['../../../green_function_large_scale/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function_large_scale/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function_large_scale/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    nlin_pars = res_reader.nlin_pars,
    nlin_par_names = ['log10(visM)','log10(He)','rake'],
    file_incr_slip0 = '../../incr_slip0_respacing.h5',
    )

pred.save('partition_large_scale.h5')
##
##writer = vj.inv.PredDispToDatabaseWriter(
##    pred_disp = pred
##    )
##
##writer.create_database()
##writer.insert_all()

