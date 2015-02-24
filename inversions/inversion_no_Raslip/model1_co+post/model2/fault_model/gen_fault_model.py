import os
from os.path import exists

from viscojapan.fault_model.control_points import control_points3
from viscojapan.fault_model import SubfaultsMeshesByLength

import viscojapan as vj

dep = 120

fault_file = 'fault_bott%dkm.h5'%dep

gen_subfault = SubfaultsMeshesByLength(
    control_points = control_points3,
    subflt_sz_dip = 25.,
    depth_bottom_limit = dep,
    subflt_sz_strike = 25.
    )
gen_subfault.save_fault_file(fault_file )
