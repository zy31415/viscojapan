import sqlite3

import numpy as np

import viscojapan as vj

import sys
sys.path.append('../../')
from epochs import epochs

num_epochs = len(epochs)

pred = vj.inv.DispPred(
    G_file = '../../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    filter_sites_file = '../../sites_2EXPs',
    result_file = '../../outs/nrough_06.h5',
    )

# save prediction
writer = vj.inv.PredDispToDatabaseWriter(
    pred_disp = pred
    )

writer.create_database()
writer.insert_all()

# save observation
writer = vj.inv.ObsToDatabaseWriter(
    file_cumu_disp_obs = '../../../obs/cumu_post_with_seafloor.h5'
    )
writer.create_database()
writer.insert_cumu_disp_obs()
