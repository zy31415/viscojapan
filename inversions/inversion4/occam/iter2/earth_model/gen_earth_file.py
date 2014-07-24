from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He33km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_bott33km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 5.839838E+18
visM1 = 1.0E+19
visM2 = 1.1E+19
visM3 = 1.2E+19

gen = GenerateEarthModelFile(
    raw_file = raw_file_He33km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save('He33km_Vis5.8E18/earth.model_He33km_Vis5.8E18')


gen = GenerateEarthModelFile(
    raw_file = raw_file_He33km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM1,    
    )
gen.save('He33km_Vis1.0E19/earth.model_He33km_Vis1.0E19')

gen = GenerateEarthModelFile(
    raw_file = raw_file_He33km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM2,    
    )
gen.save('He33km_Vis1.1E19/earth.model_He33km_Vis1.1E19')

gen = GenerateEarthModelFile(
    raw_file = raw_file_He33km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM3,    
    )
gen.save('He33km_Vis1.2E19/earth.model_He33km_Vis1.2E19')

