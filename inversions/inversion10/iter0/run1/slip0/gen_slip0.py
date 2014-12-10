import viscojapan as vj
from scipy import interpolate
import numpy as np
from pylab import plt

reader = vj.inv.ResultFileReader('./nco_06_naslip_09.h5')
slip, lon, lat = reader.read_3d_slip('fault_bott60km.h5')
epochs = reader.epochs

def _interpolate(slip, lon, lat):
    fault_file = '../../fault_model/fault_bott120km.h5'
    reader = vj.FaultFileReader(fault_file)
    lon0 = reader.LLons_mid
    lat0 = reader.LLats_mid

    points = [(x,y) for x, y in zip(np.nditer(lon),
                                    np.nditer(lat))]

    points0 = [(x,y) for x, y in zip(np.nditer(lon0),
                                    np.nditer(lat0))]
    return interpolate.griddata(points, slip.flatten(),
                                points0, fill_value=0)

with vj.EpochalFileWriter('slip0.h5') as writer:
    for si, epoch in zip(slip, epochs):
        s_new = _interpolate(si, lon, lat)
        writer[int(epoch)] = s_new.reshape([-1,1])


    
    
    

    
    
    
