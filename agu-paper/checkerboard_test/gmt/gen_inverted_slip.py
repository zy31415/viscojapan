import numpy as np

import viscojapan as vj

reader = vj.inv.ResultFileReader('dip4_stk4_ano_11.h5')

slip = reader.get_slip()

slip = slip.get_coseismic_slip()
##

fault_file = 'fault_bott80km.h5'
flt_reader = vj.fm.FaultFileReader(fault_file)
lats = flt_reader.LLats_mid
lons = flt_reader.LLons_mid

   
with open('_inverted_slip.txt','wt') as fid:
    for lon, lat, s in zip(np.nditer(lons),
                           np.nditer(lats),
                           np.nditer(slip),
                           ):
        fid.write('%f %f %f\n'%(lon,lat,s))
##
