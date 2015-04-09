import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.fault_model import FaultFileReader
import viscojapan as vj

FNULL = open(os.devnull, 'w')

fid = FaultFileReader('../fault_model/fault_bott80km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

# l_max ~= 2*pi*R/He
lmax = 850

model_str = 'standard_model/'

cm1 = stat0A(
    earth_model_stat = 'standard_model/earth.model',
    stat0_out = join(model_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cm2 = vj.pollitz.ComputeEarthModelVISCO1D(
    earth_file = 'standard_model/earth.model',
    l_max = lmax,
    outputs_dir = model_str,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

cm1()
cm2()

