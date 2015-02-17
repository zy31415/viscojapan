import numpy as np

import date_conversion as dc

import viscojapan as vj

t_eq = 55631

def fit_post(site):
    '''
cc - components code
pm - postseismic mode
'''
    tp = np.loadtxt('../post_offsets/%s.post'%site)

    t = dc.asmjd([ii[0] for ii in tp])
    eres = [ii[1] for ii in tp]
    eressd = np.ones_like(eres)
    
    nres = [ii[2] for ii in tp]
    nressd = np.ones_like(nres)
    
    ures = [ii[3] for ii in tp]
    uressd = np.ones_like(ures)
    
    cf_list=[]        

    cc = 7
    pm = '2EXPs'
    
    if cc==6:
        cstr='en'
    if cc==7:
        cstr='enu'

    for cmpt in cstr:
        yres=locals()[cmpt+'res']

        func=vj.tsana.tsmodel.Fc()

        func.cmpt=cmpt.upper()
                
        if pm=='EXP':           
            f_exp=vj.tsana.tsmodel.SubFcEXP()
            f_exp.T0=t_eq
            f_exp.am= 1.
            f_exp.tau=20.
            f_exp.tag='EXP'
            func.add_subf(f_exp)

        elif pm=='2EXPs':
            f_exp1 = vj.tsana.tsmodel.SubFcEXP()
            f_exp1.T0 = t_eq
            f_exp1.am = 1.
            f_exp1.tau = 10.
            f_exp1.tag = 'EXP1'
            func.add_subf(f_exp1)

            f_exp2 = vj.tsana.tsmodel.SubFcEXP()
            f_exp2.T0 = t_eq
            f_exp2.am = 1.
            f_exp2.tau = 1000.
            f_exp2.tag = 'EXP2'
            func.add_subf(f_exp2)

        data = vj.tsana.tsmodel.Data()
        data.set_data((t, yres, locals()[cmpt+'ressd']))
                
        cf = vj.tsana.tsmodel.IndepMLReg()
        cf.func=func
        cf.data=data
        cf.SITE=site+'-res'
        cf.CMPT=cmpt
        cf_list.append(cf)

    cfs = vj.tsana.tsmodel.JointMLReg(cf_list)

    cfs.SITE=site
    cfs.max_step=1000
    cfs.post_model = pm
    cfs.component_code = cc

    return cfs

def predict(cfs, days):
    days = np.asarray(days)
    out = []
    for cf in cfs:
        out.append(cf._func(days+t_eq))
    return out

def save_prediction(site, t, e, n, u):
    _txt = np.asarray((t,e,n,u)).T
    np.savetxt('prediction/%s.pred'%site, _txt, '%d %f %f %f',
               header = 'day e(m) n u')
    

for site in 'CHOS', 'FUKU', 'KAMN', 'KAMS', 'MYGI', 'MYGW':
    cfs = fit_post(site)
    cfs.go()
    vj.tsana.plot_post(cfs, False, loc=0,
                       save_fig_path = 'plots/',
                       file_type='pdf')
    t = range(1621)
    e, n, u = predict(cfs, t)
    save_prediction(site, t, e, n, u)
    
    

