import numpy as np

import viscojapan as vj

res_reader = vj.inv.ResultFileReader('nrough_06_naslip_11.h5')

flt_reader = vj.fm.FaultFileReader('fault_bott80km.h5')
lats = flt_reader.LLats_mid
lons = flt_reader.LLons_mid

slip = res_reader.get_slip()

coslip = slip.get_coseismic_slip()
print(np.amax(coslip))

with open('share/co_slip','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(coslip),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))


aslip = slip.get_afterslip_at_nth_epoch(-1)
with open('share/aslip_1344','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(aslip),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))
