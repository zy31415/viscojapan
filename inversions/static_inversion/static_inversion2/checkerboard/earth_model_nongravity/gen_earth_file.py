from os.path import exists
from os import makedirs

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_pollitz_He63km
from viscojapan.fault_model import FaultFileReader

fid = FaultFileReader('../fault_model/fault_bott60km.h5')
fault_bottom_depth = fid.depth_bottom

visK = inf
visM = 1.0E19
mod_str = 'He63km_VisM1.0E19'
if not exists(mod_str):
    makedirs(mod_str)
gen = GenerateEarthModelFile(
    raw_file = raw_file_pollitz_He63km,
    fault_bottom_depth = fault_bottom_depth,
    visK = visK,
    visM = visM,    
    )
gen.save(mod_str + '/earth.model_' + mod_str)


