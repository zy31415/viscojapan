import glob
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files = \
              sorted(glob.glob('../fault_model/subflts/flt_????'))

#############################

earth_file_dir = '../earth_model/earth_model_files_He45km_lmax810/'

com_He45km = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He45km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He45km',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )

###################################

earth_file_dir = '../earth_model/earth_model_files_He50km_lmax810/'

com_He50km = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He50km',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )

##################################

earth_file_dir = '../earth_model/earth_model_files_He55km_lmax810/'

com_He55km = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He55km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He55km',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )
