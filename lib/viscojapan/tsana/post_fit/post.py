from pylab import *
import re
import pickle
import os
from os.path import *

from date_conversion import *

from ..config_file_reader import ConfigFileReader
from ..pre_fit.linres_reader import LinResReader
from .tsmodel import *


t_eq = 55631

_path='../'

_dir_postres=join(_path,'post_fit/POSTRES/')
_dir_plotpost=join(_path,'post_fit/PLOTS_POST/')
_dir_cfs_post=join(_path,'post_fit/CFS_POST/')

config_reader = ConfigFileReader('../config/')

def est_am(t,y):
    """ Estimate a initial value for exponentials.
"""
    ch=t>t_eq
    y1=y[ch]
    return y1[-1]-y1[0]

def fit_post(site):
    '''
cc - components code
pm - postseismic mode
'''
    reader = LinResReader(site,'e')
    t = reader.t
    eres = reader.y
    eressd = reader.ysd

    reader = LinResReader(site,'n')
    nres = reader.y
    nressd = reader.ysd

    reader = LinResReader(site,'u')
    ures = reader.y
    uressd = reader.ysd    
    cf_list=[]

    ch=t>t_eq

    cc,pm = config_reader.get_post_model(site)
    
    if cc==6:
        cstr='en'
    if cc==7:
        cstr='enu'

    postsec = config_reader.get_postsec(site)
    jumps = config_reader.get_jumps(site, postsec)
    
    for cmpt in cstr:
        yres=locals()[cmpt+'res']

        func=Fc()

        f_cos=SubFcEq()
        f_cos.T0=t_eq
        f_cos.jump=mean(yres[ch])
        f_cos.tag='TOHOKU'
        func.add_subf(f_cos)

        func.cmpt=cmpt.upper()
        nth=1
        for jump in jumps:
            f_jump=SubFcEq()
            f_jump.T0=jump
            f_jump.jump=.01
            f_jump.tag='JUMP_%d'%nth
            func.add_subf(f_jump)
            nth+=1
        
        _am=est_am(t,yres)
        
        if pm=='EXP':           
            f_exp=SubFcEXP()
            f_exp.T0=t_eq
            f_exp.am= _am
            f_exp.tau=20.
            f_exp.tag='EXP'
            func.add_subf(f_exp)

        elif pm=='2EXPs':
            f_exp1=SubFcEXP()
            f_exp1.T0=t_eq
            f_exp1.am=_am
            f_exp1.tau=10.
            f_exp1.tag='EXP1'
            func.add_subf(f_exp1)

            f_exp2=SubFcEXP()
            f_exp2.T0=t_eq
            f_exp2.am=_am*10.
            f_exp2.tau=1000.
            f_exp2.tag='EXP2'
            func.add_subf(f_exp2)

        data=Data()
        data.t=t
        data.y0=yres
        data.y0_sd=locals()[cmpt+'ressd']
        data.cut(postsec)
        
        cf=IndepMLReg()
        cf.func=func
        cf.data=data
        cf.SITE=site+'-res'
        cf.CMPT=cmpt
        cf_list.append(cf)

    cfs=JointMLReg(cf_list)

    cfs.SITE=site
    cfs.max_step=1000
    cfs.post_model = pm
    cfs.component_code = cc

    return cfs


 
    
    
