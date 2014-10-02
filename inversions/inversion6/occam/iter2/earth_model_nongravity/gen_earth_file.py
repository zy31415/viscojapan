from os.path import exists
from os import makedirs

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He45km, raw_file_He50km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 2.7542287e+19
visM1 = 4.0E+19

def cmds(mod_str, raw_earth_file, visM):
    if not exists(mod_str):
        makedirs(mod_str)            
    gen = GenerateEarthModelFile(
        raw_file = raw_earth_file,
        fault_bottom_depth = fault_bottom_depth,
        visK = inf,
        visM = visM,    
        )
    gen.save(mod_str + '/earth.model_' + mod_str)


cmds('He50km_Vis2.8E19', raw_file_He50km, visM0)
cmds('He50km_Vis4.0E19', raw_file_He50km, visM1)
cmds('He45km_Vis2.8E19', raw_file_He45km, visM0)
