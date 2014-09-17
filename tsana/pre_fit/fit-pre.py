#!/usr/bin/env python3
''' Do linear curver fitting for one component of one stations.
'''
from os.path import exists,join
import argparse
import sys
from numpy import inf

from viscojapan.tsana.pre_fit.prermodel import _r, PreRModel
from viscojapan.tsana.pre_fit.writer_pre import Writer
from viscojapan.tsana.config_file_reader import ConfigFileReader
from viscojapan.tsana.pre_fit.plot_pre_fit import plot_pre, plt
from tenv_file_reader import read_tenv_t, read_tenv_ts, read_tenv_tssd



################3
## command line 
parser = argparse.ArgumentParser(description=__doc__)

# time series input data, required:
parser.add_argument('site_cmpt',type=str, nargs=2, help='site and cmpt')

# Output control:
parser.add_argument('--verbose','-v',action='store_true',
                    help='Verbose mode.')

parser.add_argument('--print-summary','-ps',help='Print summary.',
                    action='store_true')

parser.add_argument('--plot','-p',help='Plot.',
                    action='store_true')

args = parser.parse_args()

site = args.site_cmpt[0]
cmpt = args.site_cmpt[1]
assert cmpt in ('e', 'n', 'u')
# check time series file:
ts_dir='../raw_ts/IGS08'
f_ts=join(ts_dir,'%s.IGS08.tenv'%site)
if not exists(f_ts):
    raise ValueError('Time series file %s does not exist.'%f_ts)

#######################3
# start the program:
mod=PreRModel()

# model:
reader = ConfigFileReader('/home/zy/workspace/viscojapan/tsana/config/')
mod.if_sea = reader.if_sea(site)
mod.if_semi = reader.if_semi(site)

mod.linsecs = reader.get_linsec(site)
mod.jumps = reader.get_jumps(site,mod.linsecs)

mod.outlier_cri = reader.get_outlier_sd(site)
print(mod.outlier_cri)

# data:
mod.t=read_tenv_t(f_ts,'mjd')
mod.y=read_tenv_ts(f_ts,cmpt)
mod.ysd=read_tenv_tssd(f_ts,cmpt)
mod.lm(verbose=args.verbose)

if args.print_summary:
    print(_r('summary(fit)'))

fn = 'linres/%s.%s.lres'%(site,cmpt)
w=Writer(mod, fn)
w.title='%s %s'%(site,cmpt)
w.write()

if args.plot:        
    plot_pre(fn)
    plt.legend(loc=0)
    plt.show()
    plt.close()
    



