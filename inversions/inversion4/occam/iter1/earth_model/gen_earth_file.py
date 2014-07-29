from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He50km, raw_file_He55km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_He50km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 5.839838E+18
visM1 = 1.0E+19

## Model Zero - The original model:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 50km
# (3) rake - 90.

## Model Three - Variation on rake:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 50km
# (3) rake - 95.

gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save('He50km_Vis5.8E18/earth.model_He50km_Vis5.8E18')

## Model One - Variation on viscosity:
# (1) viscosity - 1.0E+19 Pa.s
# (2) elastic depth - 50km
# (3) rake - 90.

gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM1,    
    )
gen.save('He50km_Vis1.0E19/earth.model_He50km_Vis1.0E19')

## Model Two - Variation on elastic depth:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 55km
# (3) rake - 90.

gen = GenerateEarthModelFile(
    raw_file = raw_file_He55km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save('He55km_Vis5.8E18/earth.model_He55km_Vis5.8E18')
