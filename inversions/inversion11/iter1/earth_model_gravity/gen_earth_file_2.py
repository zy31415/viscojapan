from os.path import exists
from os import makedirs

from numpy import inf

import viscojapan as vj
from viscojapan.earth_model import raw_file_He50km, raw_file_He60km

fid = vj.fm.FaultFileReader('../fault_model/fault_bott80km.h5')
fault_bottom_depth = fid.depth_bottom


def add_task(mod_str, He, visK, visM):
    if not exists(mod_str):
        makedirs(mod_str)
    raw_earth_file = globals()['raw_file_He%02dkm'%He]
    gen = vj.em.GenerateEarthModelFile(
        raw_file = raw_earth_file,
        fault_bottom_depth = fault_bottom_depth,
        visK = visK,
        visM = visM,    
        )
    gen.save(mod_str + '/earth.model_' + mod_str)

add_task('He50km_VisM9.5E18', 50, inf, 9.5E18)
add_task('He50km_VisM9.0E18', 50, inf, 9.0E18)
add_task('He50km_VisM8.5E18', 50, inf, 8.5E18)
add_task('He50km_VisM8.0E18', 50, inf, 8.0E18)
add_task('He50km_VisM7.5E18', 50, inf, 7.5E18)
add_task('He50km_VisM7.0E18', 50, inf, 7.0E18)
