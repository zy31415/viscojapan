import numpy as np

import sqlite3

import viscojapan as vj

pred_db = '../../inversions/inversion10/iter2/run7/analysis/pred_disp/~pred_disp.db'

reader = vj.inv.PredDispToDatabaseReader(pred_db)
sites, ys = reader.get_R_co_at_epoch(1344)
es = ys[:,0]
ns = ys[:,1]
us = ys[:,2]
mag_hor = np.sqrt(es**2+ns**2)
