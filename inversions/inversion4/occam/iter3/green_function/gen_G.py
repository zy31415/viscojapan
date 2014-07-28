from glob import glob
import argparse

from numpy import inf, log10

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

################################
## Model Zero - The original model:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 33km
# (3) rake - 83.

mod_str = 'He33km_Vis5.8E18_Rake83'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))

model0 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'sites_with_seafloor',
    )

model0.extra_info ={
    'He':33,
    'visM':5.8E+18,
    'log10(visM)':log10(5.8E+18),
    'visK':inf,
    'rake':83
    }

model0.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }


## Model One - Variation on viscosity:
# (1) log10(visM) - 19
# 	viscosity - 1.1E+19 Pa.s
# (2) elastic depth - 33km
# (3) rake - 83.
mod_str = 'He33km_Vis1.1E19_Rake83'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))

model1 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'sites_with_seafloor',
    )

model1.extra_info ={
    'He':33,
    'visM':1.1E+19,
    'log10(visM)':log10(1.1E+19),
    'visK':inf,
    'rake':83
    }

model1.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

## Model Two - Variation on elastic depth:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 45km
# (3) rake - 83.
mod_str = 'He45km_Vis5.8E18_Rake83'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))
model2 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'sites_with_seafloor',
    )

model2.extra_info ={
    'He':45,
    'visM':5.8E+18,
    'log10(visM)':log10(5.8E+18),
    'visK':inf,
    'rake':83.
    }

model2.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }


## Model Three - Variation on rake:
# (1) log10(visM) - 18.8
#        visocosity - 5.839838E+18 Pa.s
# (2) elastic depth - 33km
# (3) rake - 90.
mod_str = 'He33km_Vis5.8E18_Rake90'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))
model3 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'sites_with_seafloor',
    )

model3.extra_info ={
    'He':33,
    'visM':5.8E+18,
    'log10(visM)':log10(5.8E+18),
    'visK':inf,
    'rake':90.
    }

model3.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Generate G matrix for indicated model.',
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

