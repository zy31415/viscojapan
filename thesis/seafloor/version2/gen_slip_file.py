import numpy as np

import viscojapan as vj

reader = vj.inv.SlipResultReader(
    result_file = 'nrough_05_naslip_11.h5',
    fault_file = 'fault_bott80km.h5'
    )

lats = reader.LLats_mid
lons = reader.LLons_mid
slip = reader.get_3d_cumu_slip()
aslip = reader.get_3d_afterslip()

with open('share/co_slip','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(slip[0,:,:]),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))


with open('share/aslip_1344','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(aslip[-1,:,:]),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))
