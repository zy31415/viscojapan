from glob import glob
import argparse

from numpy import inf, log10

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

cmd = {}

def add_task(mod_str, visK, visM, He, rake):        
    num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))
    model0 = PollitzOutputsToEpochalData(
        epochs = sorted(epochs),
        G_file = 'G_' + mod_str + '.h5',
        num_subflts = num_subflts,
        pollitz_outputs_dir = 'outs_' + mod_str,
        sites_file = 'stations.in',
        )

    model0.extra_info ={
        'He':He,
        'visM':visM,
        'log10(visM)':log10(visM),
        'visK':visK,
        'log10(visK)':log10(visK),
        'rake':rake
        }

    model0.extra_info_attrs ={
        'He':{'unit':'km'},
        'visM':{'unit':'Pa.s'},
        'visK':{'unit':'Pa.s'},
        }
    cmd[mod_str] = model0


add_task('He50km_Vis2.8E19_Rake90', inf, 2.754229E+19, 50, 90.)
add_task('He50km_Vis4.0E19_Rake90', inf, 4.0E+19, 50, 90.)
add_task('He45km_Vis2.8E19_Rake90', inf, 2.754229E+19, 45, 90.)
add_task('He50km_Vis2.8E19_Rake85', inf, 2.754229E+19, 50, 85.)

###################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate G matrix.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Generate G matrix for indicated model.',
                        )
    args = parser.parse_args()
    model = args.model[0]

    if model == 'all':
        for s,c in cmd.items():
            print(s)
            c()
    else:
        cmd[model]()

