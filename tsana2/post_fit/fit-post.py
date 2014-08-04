#!/usr/bin/env python3
import argparse

from viscojapan.tsana.post_fit.post import fit_post
from viscojapan.tsana import plot_post, save_cumu_post_disp
from viscojapan.tsana.post_fit.cumu_post import save_cumu_post
from viscojapan.tsana.post_fit.writer_residual import ResidualWriter

from days_after_mainshock import days

parser=argparse.ArgumentParser(description=''' Do postseismic curve fitting.
1. Do postseismic curve fitting.
2. Make the plot.
''')
parser.add_argument('site',type=str,nargs=1,help='site that is used to do curve fitting.')
parser.add_argument('-p',action='store_true',help='Plot the resutls.')

args = parser.parse_args()

site=args.site[0]
cfs=fit_post(site)
cfs.go()
cfs.save('cfs/%s.cfs'%site)
ResidualWriter(cfs).save('post_res/%s.post'%site)

save_cumu_post(cfs, days, 'cumu_post_displacement/%s.cumu'%site)

if args.p:
    plot_post(cfs,True)
else:
    plot_post(cfs,False)


