from numpy import inf

import viscojapan as vj

fid = vj.FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom

visM0 = 5.839838E+18
visM1 = 1.0E+19

gen = vj.GenerateEarthModelFile(
    raw_file = vj.raw_file_pollitz_He63km,
    fault_bottom_depth = fault_bottom_depth,
    visK = inf,
    visM = visM0,    
    )
gen.save('pollitz_He63km/earth.model_pollitz_He63km')
