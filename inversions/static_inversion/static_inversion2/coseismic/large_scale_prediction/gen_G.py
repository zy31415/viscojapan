from glob import glob
import argparse

from numpy import inf, log10
import numpy as np

from viscojapan.pollitz import PollitzOutputsToEpochalData
import viscojapan as vj

num_subflts = len(glob('outs/day_0000_flt_????.out'))

He = 50
visM = np.nan
visK = np.nan
rake = 83.

cmd = PollitzOutputsToEpochalData(
    epochs = [0],
    G_file = 'G.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs/',
    sites_file = 'sites.in',
    extra_info ={
    'He':He,
    'visM':visM,
    'log10(visM)':log10(visM),
    'visK':visK,
    'log10(visK)':log10(visK),
    'rake':rake
    },
    extra_info_attrs ={
    'He':{'unit':'km'},
    'visM':{'unit':'Pa.s'},
    'visK':{'unit':'Pa.s'},
    },       
    )

cmd()
