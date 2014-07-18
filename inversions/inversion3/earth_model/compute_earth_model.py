import os
from os.path import join

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.pollitz import ComputeEarthModelVISCO1D
from viscojapan.fault_model import FaultFileIO

FNULL = open(os.devnull, 'w')

fid = FaultFileIO('../fault_model/fault_He50km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

######################
earth_file_dir = 'earth_model_files_He45km/'

cmd1_He45km = stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He45km'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He45km = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He45km'),
    l_max = 810,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
earth_file_dir = 'earth_model_files_He50km/'

cmd1_He50km = stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He50km'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He50km = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He50km'),
    l_max = 810,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )

######################
earth_file_dir = 'earth_model_files_He55km/'

cmd1_He55km = stat0A(
    earth_model_stat = join(earth_file_dir, 'earth.model_He55km'),
    stat0_out = join(earth_file_dir, 'stat0.out'),
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = fault_bottom_depth,
    fault_top_depth = fault_top_depth,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = FNULL
    )

cmd2_He55km = ComputeEarthModelVISCO1D(
    earth_file = join(earth_file_dir, 'earth.model_He55km'),
    l_max = 810,
    outputs_dir = earth_file_dir,
    if_skip_on_existing_output = True,
    stdout = FNULL,
    stderr = FNULL,
    )


