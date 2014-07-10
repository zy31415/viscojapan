#!/usr/bin/env python3
from numpy import inf, log10

import sys
sys.path.append('/home/zy/workspace/greens/lib/')
from greens.pollitz_outputs_to_epoch_file import PollitzOutputsToEpochalData

reform = PollitzOutputsToEpochalData('G.h5')

# intializing the object:
reform.days_of_epochs = range(0,1201,60)
reform.no_of_subfaults = 250
reform.pollitz_outputs_dir = 'outs/'
reform.file_stations_in = './stations.in'

# record these info about the group of green's functions.
visM = 2E19
extra_info = {
    'He' : 50,
    'visM' : visM,
    'log10_visM' : log10(visM),
    'visK' : inf,
    'lmax' : 810
    }
extra_info_attrs = {
    'He' : {'unit':'km'},
    'visM' : {'unit':'Pa.s'},
    'visK' : {'unit':'Pa.s'}
    }

reform.extra_info = extra_info
reform.extra_info_attrs = extra_info_attrs

# go
reform()
