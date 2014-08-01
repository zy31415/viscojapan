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

    return cfs

def to_file(cfs):
    site = cfs.SITE
    cc,pm = config_reader.get_post_model(site)
    cos=[]
    ams=[]
    taus=[]
    rechisqs=[]
    for cf in cfs:
        cos.append(cf.get_p('jump','TOHOKU'))
        ams.append(cf.get_p('am'))
        taus.append(cf.get_p('tau'))
        rechisqs.append(cf.re_chisq())
    print(join(_dir_postres,'%s-post'%site))
    fid=open(join(_dir_postres,'%s-post'%site),'wt')

    if cc==6 and pm=='EXP':
        fid.write('# CO(m) : %s\n'%(''.join([' %f'%co for co in cos])))
        fid.write('#\n')
        fid.write('# TAU EXP(day):%f\n'%(taus[0]))
        fid.write('# AM EXP(m):%f %f\n'%(ams[0],ams[1]))
        fid.write('#\n')
        fid.write('# RE_CHISQ : %s\n'%(''.join([' %f'%ii for ii in rechisqs])))        
        fid.write('#  std  dyr  mjd  eres(m)  nres(m)\n')

        ys=asarray([cf.residual() for cf in cfs],'float').transpose()
        Ts=cfs[0].data.t        
        for y,t in zip(ys,Ts):
            fid.write('%s %.4f %5d %13.6E %13.6E\n'%\
                      (asstd(int(t)),asdyr(int(t)),t,y[0],y[1]))

    if cc==6 and pm=='2EXPs':
        fid.write('# CO(m) : %s\n'%(''.join([' %f'%co for co in cos])))
        fid.write('#\n')
        fid.write('# TAU EXP1(day):%f\n'%(taus[0][0]))
        fid.write('# AM EXP1(m):%f %f\n'%(ams[0][0],ams[1][0]))
        fid.write('#\n')
        fid.write('# TAU EXP2(day):%f\n'%(taus[0][1]))
        fid.write('# AM EXP2(m):%f %f\n'%(ams[0][1],ams[1][1]))
        fid.write('#\n')
        fid.write('# RE_CHISQ : %s\n'%(''.join([' %f'%ii for ii in rechisqs])))        
        fid.write('#  std  dyr  mjd  eres(m)  nres(m)\n')

        ys=asarray([cf.residual() for cf in cfs],'float').transpose()
        Ts=cfs[0].data.t        
        for y,t in zip(ys,Ts):
            fid.write('%s %.4f %5d %13.6E %13.6E\n'%\
                      (asstd(int(t)),asdyr(int(t)),t,y[0],y[1]))
    
    if cc==7 and pm=='EXP':
        fid.write('# CO(m) : %s\n'%(''.join([' %f'%co for co in cos])))
        fid.write('#\n')
        fid.write('# TAU EXP(day):%f\n'%(taus[0]))
        fid.write('# AM EXP(m):%f %f %f\n'%(ams[0],ams[1],ams[2]))
        fid.write('#\n')
        fid.write('# RE_CHISQ : %s\n'%(''.join([' %f'%ii for ii in rechisqs])))        
        fid.write('#  std  dyr  mjd  eres(m)  nres(m)  ures(m)\n')

        ys=asarray([cf.residual() for cf in cfs],'float').transpose()
        Ts=cfs[0].data.t        
        for y,t in zip(ys,Ts):
            fid.write('%s %.4f %5d %13.6E %13.6E %13.6E\n'%\
                      (asstd(int(t)),asdyr(int(t)),t,y[0],y[1],y[2]))
    
    if cc==7 and pm=='2EXPs':
        fid.write('# CO(m) : %s\n'%(''.join([' %f'%co for co in cos])))
        fid.write('#\n')
        fid.write('# TAU EXP1(day):%f\n'%(taus[0][0]))
        fid.write('# AM EXP1(m):%f %f %f\n'%(ams[0][0],ams[1][0],ams[2][0]))
        fid.write('#\n')
        fid.write('# TAU EXP2(day):%f\n'%(taus[0][1]))
        fid.write('# AM EXP2(m):%f %f %f\n'%(ams[0][1],ams[1][1],ams[2][1]))
        fid.write('#\n')
        fid.write('# RE_CHISQ : %s\n'%(''.join([' %f'%ii for ii in rechisqs])))        
        fid.write('#  std  dyr  mjd  eres(m)  nres(m)  ures(m)\n')

        ys=asarray([cf.residual() for cf in cfs],'float').transpose()
        Ts=cfs[0].data.t        
        for y,t in zip(ys,Ts):
            fid.write('%s %.4f %5d %13.6E %13.6E %13.6E\n'%\
                      (asstd(int(t)),asdyr(int(t)),t,y[0],y[1],y[2]))
    
    fid.close()

    return cfs   
    

def save_cfs(cfs):
    site=cfs[0].SITE
    with open(_dir_cfs_post+'%s.cfs'%site,'wb') as fid:
        pickle.dump(cfs,fid)

def plot_post(cfs,ifshow=False,path=_dir_plotpost,picfmt='png',loc=2):
    for cf in cfs:
        plot_cf(cf, color='blue')
        legend(loc=loc)
        if ifshow:
            show()

    
    
