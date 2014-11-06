from os.path import exists
from os import makedirs

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He50km, raw_file_He40km
import viscojapan as vj


fid = vj.FaultFileReader('../fault_model/fault_bott60km.h5')
fault_bottom_depth = fid.depth_bottom


def add_task(mod_str, He, visK, visM):
    if not exists(mod_str):
        makedirs(mod_str)
    raw_earth_file = globals()['raw_file_He%02dkm'%He]
    gen = GenerateEarthModelFile(
        raw_file = raw_earth_file,
        fault_bottom_depth = fault_bottom_depth,
        visK = visK,
        visM = visM,    
        )
    gen.save(mod_str + '/earth.model_' + mod_str)

add_task('He50km_VisM6.3E18', 50, inf, 6.3E18)
add_task('He50km_VisM1.0E19', 50, inf, 1.0E19)
add_task('He40km_VisM6.3E18', 40, inf, 6.3E18)
