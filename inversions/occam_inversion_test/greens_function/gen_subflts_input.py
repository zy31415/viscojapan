from viscojapan.pollitz import gen_subflts_input_for_pollitz

import argparse

parser = argparse.ArgumentParser(description='Generate subflts according to rake.')
parser.add_argument('--rake', type=int, nargs=1,
                   help='Rake angle in integer')

args = parser.parse_args()

rake =args.rake[0]

gen_subflts_input_for_pollitz(
    fault_file = 'fault_He50km.h5',
    out_dir = 'subflts_rake%02d'%rake,
    rake = rake)

