import os
from os.path import join

import viscojapan as vj
from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.pollitz import ComputeEarthModelVISCO1D
from viscojapan.fault_model import FaultFileIO

FNULL = open(os.devnull, 'w')

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

earth_file_dir = 'pollitz_He63km/'

cmd = stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_pollitz_He63km'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd()
