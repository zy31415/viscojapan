from glob import glob
import argparse

import numpy as np
from numpy import inf, log10

from viscojapan.pollitz import PollitzOutputsToEpochalData

epochs = [0]

mod_str = 'He63km_Rake81'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))

model0 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'stations.in',
    )

model0.extra_info ={
    'He':63.,
    'visM':np.nan,
    'log10(visM)':np.nan,
    'visK':np.nan,
    'rake':81.
    }

model0.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

mod_str = 'He63km_Rake90'
num_subflts = len(glob('outs_' +mod_str+ '/day_0000_flt_????.out'))

model1 = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G_' + mod_str + '.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs_' + mod_str,
    sites_file = 'stations.in',
    )

model1.extra_info ={
    'He':63.,
    'visM':np.nan,
    'log10(visM)':np.nan,
    'visK':np.nan,
    'rake':90.
    }

model1.extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    }

model0()
#model1()
