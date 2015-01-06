import sqlite3

import numpy as np

import viscojapan as vj

pred = vj.inv.DispPred(
    file_G0 = '../../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    result_file = '../../outs/nrough_06_naslip_10.h5',
    fault_file = '../../../fault_model/fault_bott80km.h5',
    files_Gs = ['../../../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                '../../../green_function/G2_He60km_VisM6.3E18_Rake83.h5',
                '../../../green_function/G3_He50km_VisM6.3E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','log10(He)','rake'],
    file_incr_slip0 = '../../slip0/v1/slip0.h5',
    )

writer = vj.inv.PredDispToDatabaseWriter(
    pred_disp = pred
    )

writer.create_database()
writer.insert_all()

