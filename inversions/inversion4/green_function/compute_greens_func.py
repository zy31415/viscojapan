import glob
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_rake90/flt_????'))

subflts_files_rake95 = \
              sorted(glob.glob('../fault_model/subflts_rake95/flt_????'))

#############################
## Model Zero - The original model:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 50km
# (3) rake - 90.

## Model One - Variation on viscosity:
# (1) viscosity - 1.0E+19 Pa.s
# (2) elastic depth - 50km
# (3) rake - 90.

earth_file_dir = '../earth_model/He50km_Vis1.0E19/'

model_He50km_Vis1E19_Rake90 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km_Vis1.0E19'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He50km_Vis1.0E19_Rake90',
    subflts_files = subflts_files_rake90,
    controller_file = 'pool.config',
    )

## Model Two - Variation on elastic depth:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 55km
# (3) rake - 90.

## Model Three - Variation on rake:
# (1) viscosity - 5.839838E+18 Pa.s
# (2) elastic depth - 50km
# (3) rake - 95.

earth_file_dir = '../earth_model/He50km_Vis5.8E18/'

model_He50km_Vis5_8E18_Rake95 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km_Vis5.8E18'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He50km_Vis5.8E18_Rake95',
    subflts_files = subflts_files_rake95,
    controller_file = 'pool.config',
    )

