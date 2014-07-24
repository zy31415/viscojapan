import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

parser = argparse.ArgumentParser(
    description="Compute green's function according to rake.")
parser.add_argument('--rake', type=int, nargs=1,
                   help='Rake angle in integer')

args = parser.parse_args()

rake =args.rake[0]

epochs = [0]

subflts_files = \
              sorted(glob.glob('subflts_rake%02d/flt_????'%rake))

earth_file_dir = '../earth_model/He50km_Vis5.8E18/'

model1 = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'sites_with_seafloor',
    earth_file = join(earth_file_dir, 'earth.model_He50km_Vis5.8E18'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs_Rake%02d'%rake,
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )

model1()
