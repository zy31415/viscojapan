import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.fault_model import FaultFileReader
import viscojapan as vj

FNULL = open(os.devnull, 'w')

fid = FaultFileReader('../fault_model/fault_bott60km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

model_str = 'He63km_VisM1.0E19'

cmd = stat0A(
    earth_model_stat = join(model_str, 'earth.model_'+model_str),
    stat0_out = join(model_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd.run()
