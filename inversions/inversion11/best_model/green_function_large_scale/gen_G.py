from glob import glob
import argparse

from numpy import inf, log10

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

cmd = {}

visK = inf
visM = 8.459897E18 # Pa.s
He = 47.17 # km
rake = 83.98

num_subflts = len(glob('outs/day_0000_flt_????.out'))

model = PollitzOutputsToEpochalData(
    epochs = sorted(epochs),
    G_file = 'G_large_scale.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs/',
    sites_file = 'stations_large_scale.in',
    extra_info ={
    'He':He,
    'log10(He)' : log10(He),
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


###################################
if __name__ == '__main__':
    model()
