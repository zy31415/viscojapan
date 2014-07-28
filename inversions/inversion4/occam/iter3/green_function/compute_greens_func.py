import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files_rake83 = \
              sorted(glob.glob('../fault_model/subflts_bott33km_rake83/flt_????'))

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_bott33km_rake90/flt_????'))

#############################
## Model Zero - The original model:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 33km
# (3) rake - 83.

mod_str = 'He33km_Vis5.8E18'
earth_file_dir = join('../earth_model/', mod_str)

model0 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_'+mod_str+'_Rake83',
    subflts_files = subflts_files_rake83,
    controller_file = 'pool.config',
    )

## Model One - Variation on viscosity:
# (1) log10(visM) - 19
# 	viscosity - 1.0E+19 Pa.s
# (2) elastic depth - 33km
# (3) rake - 83.

mod_str = 'He33km_Vis1.1E19'
earth_file_dir = join('../earth_model/', mod_str)

model1 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_'+mod_str+'_Rake83',
    subflts_files = subflts_files_rake83,
    controller_file = 'pool.config',
    )

## Model Two - Variation on elastic depth:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 45km
# (3) rake - 83.

mod_str = 'He45km_Vis5.8E18'
earth_file_dir = join('../earth_model/', mod_str)

model2 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_'+mod_str+'_Rake83',
    subflts_files = subflts_files_rake83,
    controller_file = 'pool.config',
    )

## Model Three - Variation on rake:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 33km
# (3) rake - 90.

mod_str = 'He33km_Vis5.8E18'
earth_file_dir = join('../earth_model/', mod_str)

model3 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_'+mod_str+'_Rake90',
    subflts_files = subflts_files_rake90,
    controller_file = 'pool.config',
    )

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute G matrix for indicated model.',
                        choices = ['model0','model1','model2','model3'],
                        )
    args = parser.parse_args()
    model = args.model[0]

    if model == 'model0':
        model0()
    elif model == 'model1':
        model1()
    elif model == 'model2':
        model2()
    elif model == 'model3':
        model3()
    else:
        raise ValueError('Wrong options.')
