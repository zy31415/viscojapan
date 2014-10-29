import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files_rake80 = \
              sorted(glob.glob('../fault_model/subflts_rake80/flt_????'))

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_rake90/flt_????'))

cmd = {}

def add_task(mod_str, rake, model_num):
    earth_file_dir = join('../earth_model_nongravity/', mod_str)
    subflts_files = globals()['subflts_files_rake%02d'%rake]
    model = ComputeGreensFunction(
        epochs = epochs,
        file_sites = 'stations.in',
        earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
        earth_file_dir = earth_file_dir,
        outputs_dir = 'outs%d_'%model_num + mod_str+'_Rake%2d'%rake,
        subflts_files = subflts_files,
        controller_file = 'pool.config',
        )
    cmd['%d'%model_num] = model

add_task('He63km_VisM1.0E19', 90, 0)
add_task('He63km_VisM1.0E19', 80, 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute G matrix for indicated model.'
                        )
    args = parser.parse_args()
    model = args.model[0]
    cmd[model]()