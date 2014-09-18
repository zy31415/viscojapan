import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_rake90/flt_????'))

subflts_files_rake81 = \
              sorted(glob.glob('../fault_model/subflts_rake81/flt_????'))

# compute Green's function for coseismic slip only
epochs = [0.]

earth_file_dir = '../earth_model/pollitz_He63km/'

model0 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_pollitz_He63km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He63km_Rake90',
    subflts_files = subflts_files_rake90,
    controller_file = 'pool.config',
    )

model1 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_pollitz_He63km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He63km_Rake81',
    subflts_files = subflts_files_rake81,
    controller_file = 'pool.config',
    )

model0()
model1()
