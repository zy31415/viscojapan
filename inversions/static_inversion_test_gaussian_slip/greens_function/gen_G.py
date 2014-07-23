from glob import glob
import argparse

from numpy import inf

from viscojapan.pollitz import PollitzOutputsToEpochalData


mod_str = 'Rake80'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))

model0 = PollitzOutputsToEpochalData(
    epochs = [0],
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'sites_with_seafloor',
    )

model0.extra_info ={
    'He':50,
    'visM':5.8E+18,
    'visK':inf,
    'rake':80
    }

model0.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

model0()
