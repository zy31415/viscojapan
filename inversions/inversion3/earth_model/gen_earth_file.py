from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He45km, raw_file_He50km, raw_file_He55km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_He50km.h5')
fault_bottom_depth = fid.depth_bottom

visM = 5.839838E+18

gen = GenerateEarthModelFile(
    raw_file = raw_file_He45km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM,    
    )
gen.save('earth_model_files_He45km/earth.model_He45km')

gen = GenerateEarthModelFile(
    raw_file = raw_file_He50km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM,    
    )
gen.save('earth_model_files_He50km/earth.model_He50km')

gen = GenerateEarthModelFile(
    raw_file = raw_file_He55km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM,    
    )
gen.save('earth_model_files_He55km/earth.model_He55km')
