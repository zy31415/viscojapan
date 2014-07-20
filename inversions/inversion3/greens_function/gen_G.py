from glob import glob
import argparse

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

if args.model == 'He45km':
    gen_G_He45km()
elif args.model == 'He50km':
    gen_G_He50km()
elif args.model == 'He55km':
    gen_G_He55km()

