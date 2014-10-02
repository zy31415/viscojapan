import os

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He50km, raw_file_He55km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 1E+19
visM1 = 2E+19

visK0 = 5E+17
visK1 = 6E+17

# model 0
gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = visK0,
    visM = visM0,    
    )
model_str = 'He50km_VisK5.0E17_VisM1.0E19'
if not os.path.exists(model_str):
    os.makedirs(model_str)
gen.save(model_str + '/earth.model_' + model_str)

# model 1
gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = visK1,
    visM = visM0,    
    )
model_str = 'He50km_VisK6.0E17_VisM1.0E19'
if not os.path.exists(model_str):
    os.makedirs(model_str)
gen.save(model_str + '/earth.model_' + model_str)

# model 3
gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = visK0,
    visM = visM1,    
    )
model_str = 'He50km_VisK5.0E17_VisM2.0E19'
if not os.path.exists(model_str):
    os.makedirs(model_str)
gen.save(model_str + '/earth.model_' + model_str)
