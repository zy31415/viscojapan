from viscojapan.fault_model import \
     SubfaultsMeshesByLength

gen_subfault = SubfaultsMeshesByLength(
    subflt_sz_dip = 20.,
    depth_bottom_limit = 50.,
    subflt_sz_strike = 20.
    )

gen_subfault.save_fault_file('fault_He50km.h5')


