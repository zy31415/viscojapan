from os.path import exists
from os import makedirs

from numpy import inf

from viscojapan.earth_model import GenerateEarthModelFile, \
     raw_file_He50km, raw_file_He55km
from viscojapan.fault_model import FaultFileIO

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
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

add_task('He50km_VisK5.0E17_VisM1.0E19', 50, 5.0E17, 1.0E19)
add_task('He50km_VisK6.0E17_VisM1.0E19', 50, 6.0E17, 1.0E19)
add_task('He50km_VisK5.0E17_VisM2.0E19', 50, 5.0E17, 2.0E19)
add_task('He55km_VisK5.0E17_VisM1.0E19', 55, 5.0E17, 1.0E19)
