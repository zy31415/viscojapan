#!/usr/bin/env python3

import sys
sys.path.append('/home/zy/workspace/greens/lib/')

from greens.gfilter import GFilter

# initialization:
gfilter = GFilter()
gfilter.G_old = 'G.h5'
gfilter.G_new = 'filter_G.h5'
gfilter.sites_file = 'sites'

# go
gfilter()
