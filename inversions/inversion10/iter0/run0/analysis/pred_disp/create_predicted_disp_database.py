import sqlite3

import numpy as np

import viscojapan as vj

import sys
sys.path.append('../../')
from epochs import epochs

num_epochs = len(epochs)

pred = vj.inv.DispPred(
    G_file = '../../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    result_file = '../../outs/nrough_06.h5',
    fault_file = '../../../fault_model/fault_bott120km.h5',
    )

writer = vj.inv.PredDispToDatabaseWriter(
    pred_disp = pred
    )

writer.create_database()
writer.insert_all()
