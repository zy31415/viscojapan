import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

epochs = [0]

subflts_files_rake80 = \
              sorted(glob.glob('../fault_model/subflts_rake80/flt_????'))

earth_file_dir = '../earth_model/He50km_Vis5.8E18/'

model1 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km_Vis5.8E18'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_Rake90',
    subflts_files = subflts_files_rake80,
    controller_file = 'pool.config',
    )

model1()
