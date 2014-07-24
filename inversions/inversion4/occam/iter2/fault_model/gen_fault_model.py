from viscojapan.fault_model.control_points import control_points2
from viscojapan.fault_model import SubfaultsMeshesByLength

gen_subfault = SubfaultsMeshesByLength(
    control_points = control_points2,
    subflt_sz_dip = 20.,
    depth_bottom_limit = 33.,
    subflt_sz_strike = 20.
    )

gen_subfault.save_fault_file('fault_bott33km.h5')
