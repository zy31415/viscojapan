from os.path import exists
from os import makedirs

from numpy import inf

import viscojapan as vj


raw_file = 'earth.modelBURG-SUM_47.17km'

fid = vj.fm.FaultFileReader('../fault_model/fault_bott80km.h5')
fault_bottom_depth = fid.depth_bottom


visK = inf
visM = 10**18.92736508263518

gen = vj.em.GenerateEarthModelFile(
    raw_file = raw_file,
    fault_bottom_depth = fault_bottom_depth,
    visK = visK,
    visM = visM,    
    )

gen.save('standard_model/earth.model')
