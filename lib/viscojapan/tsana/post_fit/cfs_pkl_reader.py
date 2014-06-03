''' This module provide functions read pickled cfs file
to get time series modelgprediction.
'''
from pylab import *
from os.path import join
import pickle
from ..config_file_reader import ConfigFileReader

_dir_cfs_post='CFS_POST'

t_eq=55631

def get_cos(site):
    ''' Get displacements of sites.
'''
    site=site.decode()
    with open(join(_dir_cfs_post,site+'-res.cfs'),'rb') as fid:
        cfs=pickle.load(fid)
        
    co0=cfs[0].get_subf('TOHOKU').jump
    co1=cfs[1].get_subf('TOHOKU').jump
    if len(cfs.cfs)==2:
        co2=nan
    else:
        co2=cfs[2].get_subf('TOHOKU').jump
    return asarray([co0,co1,co2],'float')

config_reader = ConfigFileReader()

def get_post(site,t):
    ''' Get displacements of sites at certain time epoch.
'''
    post=[]
    site=site.decode()
    with open(join(_dir_cfs_post,site+'-res.cfs'),'rb') as fid:
        cfs=pickle.load(fid)
    pm = config_reader.get_post_model(site)[1]
    tp=[nan]*3
    for cf in cfs:
        if pm=='EXP':
            f=cf.get_subf('EXP')
        elif pm=='2EXPs':
            f=lambda t: cf.get_subf('EXP1')(t)+\
               cf.get_subf('EXP2')(t)
        else:
            raise ValueError('Post model not reconized.')

        if cf.CMPT=='e':
            tp[0]=f(t+t_eq)[0]
        elif cf.CMPT=='n':
            tp[1]=f(t+t_eq)[0]
        elif cf.CMPT=='u':
            tp[2]=f(t+t_eq)[0]
        else:
            raise ValueError('CMPT not recongnized.')
    return asarray(tp,'float')

if __name__=='__main__':
    #cos=get_cos()
    post=get_post(1000)

