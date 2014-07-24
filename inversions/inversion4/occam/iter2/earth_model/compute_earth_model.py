import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.pollitz import ComputeEarthModelVISCO1D
from viscojapan.fault_model import FaultFileIO

FNULL = open(os.devnull, 'w')

fid = FaultFileIO('../fault_model/fault_bott33km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

lmax = 1220

######################
earth_file_dir = 'He33km_Vis5.8E18/'

cmd1_He33km_Vis5_8E18= stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He33km_Vis5.8E18'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He33km_Vis5_8E18 = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He33km_Vis5.8E18'),
    l_max = lmax,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
earth_file_dir = 'He33km_Vis1.0E19/'

cmd1_He33km_Vis1_0E19= stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He33km_Vis1.0E19'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He33km_Vis1_0E19 = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He33km_Vis1.0E19'),
    l_max = lmax,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
earth_file_dir = 'He33km_Vis1.1E19/'

cmd1_He33km_Vis1_1E19= stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He33km_Vis1.1E19'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He33km_Vis1_1E19 = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He33km_Vis1.1E19'),
    l_max = lmax,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
earth_file_dir = 'He33km_Vis1.2E19/'

cmd1_He33km_Vis1_2E19= stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He33km_Vis1.2E19'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He33km_Vis1_2E19 = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He33km_Vis1.2E19'),
    l_max = lmax,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute earth model.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute earth model.',
                        choices = ['He33km_Vis5.8E18','He33km_Vis1.0E19'],
                        )
    args = parser.parse_args()
    model = args.model[0]

    if model == 'He33km_Vis5.8E18':
        cmd1_He33km_Vis5_8E18()
        cmd2_He33km_Vis5_8E18.run()
    elif model == 'He33km_Vis1.0E19':
        cmd1_He33km_Vis1_0E19()
        cmd2_He33km_Vis1_0E19.run()
    elif model == 'He33km_Vis1.1E19':
        cmd1_He33km_Vis1_1E19()
        cmd2_He33km_Vis1_1E19.run()
    elif model == 'He33km_Vis1.2E19':
        cmd1_He33km_Vis1_2E19()
        cmd2_He33km_Vis1_2E19.run()
    else:
        raise ValueError('Wrong options.')
