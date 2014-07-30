#!/usr/bin/env python3
import argparse

from viscojapan.tsana.post_fit.post import fit_post,to_file,save_cfs
from viscojapan.tsana import plot_post

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
to_file(cfs)
save_cfs(cfs)

if args.p:
    plot_post(cfs,True)
else:
    plot_post(cfs,False)


