import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

epochs = range(0,2000, 60)

subflts_files_rake90 = \
              sorted(glob.glob('../fault_model/subflts_bott80km_rake90/flt_0154'))

cmd = {}

def add_task_nongravity(mod_str, rake, mode_num):
    earth_file_dir = join('../earth_model_nongravity/', mod_str)
    subflts_files = globals()['subflts_files_rake%02d'%rake]
    cmd[mode_num] = ComputeGreensFunction(
        epochs = epochs,
        file_sites = 'near_stations.in',
        earth_file = join(earth_file_dir, 'earth.model_' + mod_str),
        earth_file_dir = earth_file_dir,
        outputs_dir = 'outs_'+mod_str+'_Rake%2d'%rake,
        subflts_files = subflts_files,
        controller_file = 'pool.config',
        )

add_task_nongravity('He50km_VisM6.3E18', 90, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute G matrix for indicated model.'
                        )
    args = parser.parse_args()
    model_num = int(args.model[0])
    cmd[model_num]()
