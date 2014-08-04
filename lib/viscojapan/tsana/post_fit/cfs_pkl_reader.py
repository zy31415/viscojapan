from os.path import join
import pickle

from numpy import asarray, nan, hstack, savetxt

from ..config_file_reader import ConfigFileReader

t_eq = 55631

def get_co(cfs):
    co0=cfs[0].get_subf('TOHOKU').jump
    co1=cfs[1].get_subf('TOHOKU').jump
    if len(cfs.cfs)==2:
        co2=nan
    else:
        co2=cfs[2].get_subf('TOHOKU').jump
    return asarray([co0,co1,co2],'float')
    

def get_post(cfs, t):
    post = []
    site = cfs.SITE
    
    pm = cfs.post_model
    tp=[0]*3
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

def get_cumu_post(cfs, t):
    return get_co(cfs) + get_post(cfs, t)

def save_cumu_post_disp(cfs, t, fn):
    t = asarray(t)
    cumu = get_cumu_post(cfs, t)
    print(t.shape)
    savetxt(fn, hstack((t.reshape([-1,1]),cumu.reshape([-1,3]))))


