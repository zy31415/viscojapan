import h5py
import numpy as np

import viscojapan as vj

from epochs import epochs

reader = vj.ResultFileReader('nrough_06.h5')
slip = reader.slip[:-3]
        
vj.break_col_vec_into_epoch_file(
    slip, epochs, epoch_file = 'slip0.h5',
    )
