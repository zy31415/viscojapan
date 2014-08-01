import re
from os.path import basename, join
import glob
import pickle

from numpy import loadtxt, isnan

def collect_value(files, reader):
    ''' The retured data structure:
val_dic[site][cmpt] = val
'''
    val_dic = {}
    for file in files:
        tp = basename(file).split('.')
        site = tp[0]
        cmpt = tp[1]
        val = reader(file)
        if site in val_dic:
            val_dic[site][cmpt] = val
        else:
            val_dic[site] = {cmpt:val}
    return val_dic


def sorted_value(val_dic, cmpt):
    def key(x):
        out = x[1][cmpt]
        if isnan(out):
            out = 0.
        return out
    return sorted(val_dic.items(), key=key, reverse=True)

def save_to_file(sorted_value, fn, value_kind):
    with open(fn,'wt') as fid:
        fid.write('# site e_{0} n_{0} u_{0} \n'.format(value_kind))
        for ii in sorted_value:
            fid.write('%s %f %f %f\n'%(
                ii[0], ii[1]['e'], ii[1]['n'], ii[1]['u']))

##def save_to_file(L, fn):
##    with open(fn,'wt') as fid:
##        fid.write('# site e_sd n_sd u_sd \n')
##        for ii in L:
##            fid.write('%s %f %f %f\n'%(
##                ii[0], ii[1]['e'], ii[1]['n'], ii[1]['u']))

##def sort_by_misfit(sd_dic, cmpt):    
##    return sorted(sd_dic.items(), key=lambda x: x[1][cmpt], reverse=True)

##def read_misfit_from_prelin_files(files, misfit_kind):
##    sd_dic = {}
##    for file in files:
##        tp = basename(file).split('.')
##        site = tp[0]
##        cmpt = tp[1]
##        if site in sd_dic:
##            sd_dic[site][cmpt] = read_misfit(file, misfit_kind)
##        else:
##            sd_dic[site] = {cmpt:read_misfit(file, misfit_kind)}
##    return sd_dic

def read_misfit_from_pickled_cfs(files):
    rms_dic = {}
    for file in files:
        with open(file, 'rb') as fid:
            cfs = pickle.load(fid)
        site = cfs.SITE
        rms_dic[site] = {}
        for cf in cfs:
            cmpt = cf.CMPT
            rms = cf.rms()*1000. # from m => mm
            rms_dic[site][cmpt] = rms

    for site, sds in rms_dic.items():
        if 'u' not in sds:
            rms_dic[site]['u']=-1
    return rms_dic
