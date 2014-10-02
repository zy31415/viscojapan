import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.pollitz import ComputeEarthModelVISCO1D
from viscojapan.fault_model import FaultFileIO

FNULL = open(os.devnull, 'w')

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

# l_max ~= 2*pi*R/He
lmax = 900

cmd1={}
cmd2={}

######################
mod_str = 'He50km_Vis2.8E19'

cmd1[mod_str]= stat0A(
    earth_model_stat = join(mod_str, 'earth.model_'+mod_str),
    stat0_out = join(mod_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2[mod_str] = ComputeEarthModelVISCO1D(
    earth_file = join(mod_str, 'earth.model_'+mod_str),
    l_max = lmax,
    outputs_dir = mod_str,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
mod_str = 'He50km_Vis4.0E19'

cmd1[mod_str]= stat0A(
    earth_model_stat = join(mod_str, 'earth.model_'+mod_str),
    stat0_out = join(mod_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2[mod_str] = ComputeEarthModelVISCO1D(
    earth_file = join(mod_str, 'earth.model_'+mod_str),
    l_max = lmax,
    outputs_dir = mod_str,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
mod_str = 'He45km_Vis2.8E19'

cmd1[mod_str]= stat0A(
    earth_model_stat = join(mod_str, 'earth.model_'+mod_str),
    stat0_out = join(mod_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2[mod_str] = ComputeEarthModelVISCO1D(
    earth_file = join(mod_str, 'earth.model_'+mod_str),
    l_max = 200,
    outputs_dir = mod_str,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
mod_str = 'He55km_Vis2.8E19'

cmd1[mod_str]= stat0A(
    earth_model_stat = join(mod_str, 'earth.model_'+mod_str),
    stat0_out = join(mod_str, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2[mod_str] = ComputeEarthModelVISCO1D(
    earth_file = join(mod_str, 'earth.model_'+mod_str),
    l_max = 730,
    outputs_dir = mod_str,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute earth model.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute earth model.',
                        )
    args = parser.parse_args()
    model = args.model[0]

    cmd1[model]()
    cmd2[model].run()