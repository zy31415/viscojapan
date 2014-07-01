from viscojapan.fault_model import SubfaultsMeshes

sf = SubfaultsMeshes()
sf.num_subflt_along_strike = 26
sf.num_subflt_along_dip = 11
sf.depth_limit = 50.

sf.save_fault_file('fault_250.h5')
