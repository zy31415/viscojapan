import glob
from os.path import join
import argparse

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files = \
              sorted(glob.glob('../fault_model/subflts/flt_????'))

#############################

earth_file_dir = '../earth_model/earth_model_files_He45km/'

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

earth_file_dir = '../earth_model/earth_model_files_He50km/'

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

earth_file_dir = '../earth_model/earth_model_files_He55km/'

com_He55km = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He55km'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_He55km',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )

###################################
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Compute Green's function")
    parser.add_argument('model', type=str, nargs=1,
                        help="Compute Green's function for indicated model.",
                        choices = ['He45km','He50km','He55km'],
                        )
    args = parser.parse_args()
    model = args.model[0]

    if model == 'He45km':
        com_He45km.run()
    elif model == 'He50km':
        com_He50km.run()
    elif model == 'He55km':
        com_He55km.run()
    else:
        raise ValueError('Wrong options.')
