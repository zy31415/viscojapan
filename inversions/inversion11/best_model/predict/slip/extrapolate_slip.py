import unittest
from os.path import join

import viscojapan as vj

from epochs import epochs

slip = vj.epoch_3d_array.Slip.load('slip.h5')

gen = vj.slip.SlipExtrapolationLOG(
    slip = slip,
    epochs = epochs,
    output_file = 'extra_slip_LOG.h5',
)
gen.go()

    
gen = vj.slip.SlipExtrapolationEXP(
    slip = slip,
    epochs = epochs,
    output_file = 'extra_slip_EXP.h5',
)
gen.go()


