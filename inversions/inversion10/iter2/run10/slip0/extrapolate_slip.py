import unittest
from os.path import join

import viscojapan as vj

epochs = list(range(0,1621, 60)) + list(range(365*5, 365*27+1, 365))

slip = vj.epoch_3d_array.Slip.load('slip0.h5')

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


