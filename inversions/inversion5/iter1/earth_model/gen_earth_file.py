from os.path import exists
from os import makedirs

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_bott40km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 5.839838E+18
visM1 = 1.1E+19


mod_str = 'He40km_Vis5.8E18'
if not exists(mod_str):
    makedirs(mod_str)
gen = GenerateEarthModelFile(
    raw_file = 'earth.modelBURG-SUM_40km',
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save(mod_str + '/earth.model_' + mod_str)


mod_str = 'He40km_Vis1.1E19'
if not exists(mod_str):
    makedirs(mod_str)
gen = GenerateEarthModelFile(
    raw_file = 'earth.modelBURG-SUM_40km',
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM1,    
    )
gen.save(mod_str + '/earth.model_' + mod_str)


mod_str = 'He45km_Vis5.8E18'
if not exists(mod_str):
    makedirs(mod_str)
gen = GenerateEarthModelFile(
    raw_file = 'earth.modelBURG-SUM_45km',
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save(mod_str + '/earth.model_' + mod_str)
