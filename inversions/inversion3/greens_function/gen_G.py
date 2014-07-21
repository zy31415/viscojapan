from glob import glob
import argparse

from numpy import inf

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

################################
num_subflts = len(glob('outs_He45km/day_0000_flt_????.out'))

gen_G_He45km = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_He45km.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_He45km/',
    sites_file = 'sites_with_seafloor',
    )
gen_G_He45km.extra_info ={
    'He':45,
    'visM':5.839838E+18,
    'visK':inf,
    }
gen_G_He45km.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

################################
num_subflts = len(glob('outs_He50km/day_0000_flt_????.out'))

gen_G_He50km = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_He50km.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_He50km/',
    sites_file = 'sites_with_seafloor',
    )

################################
num_subflts = len(glob('outs_He55km/day_0000_flt_????.out'))

gen_G_He55km = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_He55km.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_He55km/',
    sites_file = 'sites_with_seafloor',
    )

###################################
parser = argparse.ArgumentParser(description='Generate G matrix.')
parser.add_argument('model', type=str, nargs=1,
                    help='Generate G matrix for indicated model.',
                    choices = ['He45km','He50km','He55km'],
                    )
args = parser.parse_args()
model = args.model[0]

if model == 'He45km':
    gen_G_He45km()
elif model == 'He50km':
    gen_G_He50km()
elif model == 'He55km':
    gen_G_He55km()
else:
    raise ValueError('Wrong options.')

