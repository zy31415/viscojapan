from viscojapan.fault import SubfaultsMeshes

sf = SubfaultsMeshes()
sf.num_subflt_along_strike = 26
sf.num_subflt_along_dip = 11
sf.depth_limit = 59.72748889022895

sf.save_fault_file('fault.h5')
