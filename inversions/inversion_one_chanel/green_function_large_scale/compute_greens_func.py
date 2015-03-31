import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

epochs = epochs[1:] + [0]

subflts_files_rake83 = \
              sorted(glob.glob('../fault_model/subflts_bott80km_rake83/flt_????'))

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_bott80km_rake90/flt_????'))

cmd = {}

def add_task_nongravity(mod_str, rake, mode_num):
    earth_file_dir = join('../earth_model_nongravity/', mod_str)
    subflts_files = globals()['subflts_files_rake%02d'%rake]
    cmd[mode_num] = ComputeGreensFunction(
        epochs = epochs,
        file_sites = 'stations_large_scale.in',
        earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
        earth_file_dir = earth_file_dir,
        outputs_dir = 'outs_'+mod_str+'_Rake%2d'%rake,
        subflts_files = subflts_files,
        controller_file = 'pool.config',
        )

add_task_nongravity('He50km_VisM6.3E18', 83, 0)
add_task_nongravity('He50km_VisM1.0E19', 83, 1)
add_task_nongravity('He60km_VisM6.3E18', 83, 2)
add_task_nongravity('He50km_VisM6.3E18', 90, 3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute G matrix for indicated model.'
                        )
    args = parser.parse_args()
    model_num = int(args.model[0])
    cmd[model_num]()
