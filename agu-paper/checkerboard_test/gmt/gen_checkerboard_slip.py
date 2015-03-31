import numpy as np

import viscojapan as vj

dip_patch_size = 4
strike_patch_size = 4
fault_file = 'fault_bott80km.h5'

slip = vj.inv.test.gen_checkerboard_slip_from_fault_file(
    fault_file,
    dip_patch_size = dip_patch_size,
    strike_patch_size = strike_patch_size)

slip *= 2


flt_reader = vj.fm.FaultFileReader(fault_file)
lats = flt_reader.LLats_mid
lons = flt_reader.LLons_mid

   
with open('_checkerboard_slip.txt','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(slip),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))

