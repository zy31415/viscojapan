from numpy import loadtxt
import numpy as np

import viscojapan as vj

def read_baek_2012():
    fn = 'codisp/Baek_2012_supp_TableS1.txt'
    tp = loadtxt(fn, '5a,2f', usecols=(0,3,6,))
    out = {}
    for ii in tp:
        site = ii[0].decode()
        if site[0]=='*':
            site = site[1:]
        disp = ii[1]/1000.
        out[site] = disp        
    return out

def read_baek_2012(fn, unit='mm'):
    tp = loadtxt(fn, '5a,2f', usecols=(0,3,6,))
    out = {}
    for ii in tp:
        site = ii[0].decode()
        if site[0]=='*':
            site = site[1:]
            
        if unit=='mm':
            disp = ii[1]/1000.
        elif unit=='m':
            disp = ii[1]
        else:
            raise ValueError()
        
        out[site] = disp        
    return out

def read_zhao_2012(fn):
    tp = loadtxt(fn, '2f, 4a', usecols=(2,3,6,))
    out = {}
    for ii in tp:
        site = ii[1].decode()
        disp = ii[0]/1000.
                
        out[site] = disp        
    return out

def merge_disp_dic(dic1, dic2):
    out = dic1.copy()
    for key, val in dic2.items():
        if key not in out:
            out[key] = val
        else:
            out[key] = (out[key] + val)/2.
    return out

# Read from my estimation
reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')

disp = reader[0].reshape([-1,3])
sites = reader['sites']

disp_dic = {s.decode():d[:-1] for s, d in zip(sites, disp)}

disp_baek = read_baek_2012('codisp/Baek_2012_supp_TableS1.txt', unit='mm')
disp_wang_igs = read_baek_2012('codisp/Wang_2011_IGS.txt', unit='m')
disp_wang_teonet = read_baek_2012('codisp/Wang_2011_TEONET.txt', unit='m')

disp_zhao_cmonoc = read_zhao_2012('codisp/Zhao_2012_CMONOC.txt')
disp_zhao_igs = read_zhao_2012('codisp/Zhao_2012_IGS.txt')

disp = merge_disp_dic(disp_dic, disp_baek)
disp = merge_disp_dic(disp, disp_wang_igs)
disp = merge_disp_dic(disp, disp_wang_teonet)
disp = merge_disp_dic(disp, disp_zhao_cmonoc)
disp = merge_disp_dic(disp, disp_zhao_igs)

sites = sorted(list(disp.keys()))
pos_sites = vj.sites_db.get_pos_dic()

hor_disp_mag = np.array([(pos_sites[site][0], pos_sites[site][1],
                 np.sqrt(disp[site][0]**2 + disp[site][1]**2), site)
                for site in sites],
               dtype="f, f, f, U4")

np.savetxt('horizontal_disp_mag', hor_disp_mag, fmt=' %f %f %f %s',
           header='lon lat mag site')    
