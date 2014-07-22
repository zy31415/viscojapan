import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

epochs = [0]

subflts_files_rake66 = \
              sorted(glob.glob('+subflts_rake66/flt_????'))

earth_file_dir = '../earth_model/He50km_Vis5.8E18/'

model1 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km_Vis5.8E18'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_Rake66',
    subflts_files = subflts_files_rake66,
    controller_file = 'pool.config',
    )

model1()
