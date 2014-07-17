from pylab import plt

from viscojapan.fault_model.control_points import control_points2
from viscojapan.fault_model import SubfaultsMeshesByLength

gen_subfault = SubfaultsMeshesByLength(
    control_points = control_points2,
    subflt_sz_dip = 10.,
    depth_bottom_limit = 50.,
    subflt_sz_strike = 10.
    )

gen_subfault.save_fault_file('fault_He50km.h5')
