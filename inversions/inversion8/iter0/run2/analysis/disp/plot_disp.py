import re

import numpy as np
from pylab import plt

from viscojapan import PlotPredictedVSObservation

from epochs import epochs

import argparse

parser = argparse.ArgumentParser(description='Plot time series.')
parser.add_argument('site', nargs=1, help='site')
parser.add_argument('-p', action='store_true', help='If show the plot.')
parser.add_argument('-o', nargs='*', default=False, help='Output a file.')

args = parser.parse_args()

site = args.site[0]

tsplt = PlotPredictedVSObservation(
    site = site,
    file_obs_cumu = '/home/zy/workspace/viscojapan/tsana/post_fit/cumu_post_displacement/%s.cumu'%site,
    epochs = epochs,
    file_pred_total = 'disp_cmpts/total',
    file_pred_elastic = 'disp_cmpts/elastic',
    file_pred_Rco = 'disp_cmpts/Rco',
    file_pred_Raslip = 'disp_cmpts/Raslip',
    )

tsplt.plot()

if args.p:
    plt.show()

if args.o:
    for file in args.o:
        plt.savefig(file)
    
plt.close()

