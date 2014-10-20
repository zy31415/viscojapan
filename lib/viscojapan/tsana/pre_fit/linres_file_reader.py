from os.path import join
import os
import re

import numpy as np
from numpy import loadtxt, asarray, nan

from ...sites import get_pos_dic

__all__ = ['read_vel_sd','read_vel','gen_vel_and_vsd_file']

class LinResReader(object):
    def __init__(self,site,cmpt):
        self.dir_linres = '../pre_fit/linres/'
        self.site=site
        self.cmpt=cmpt

        # loading the data
        self._data=loadtxt(join(self.dir_linres,'%s.%s.lres'%(site,cmpt)))

    @property
    def t(self):
        ''' time
'''
        return self._data[:,0]

    @property
    def y(self):
        '''Linear residual'''
        return self._data[:,2]

    @property
    def ysd(self):
        '''Standard deviation of linear residual'''
        return self._data[:,3]

def read_t(fn):
    return asarray(loadtxt(fn)[:,0], int)

def read_y(fn):
    return asarray(loadtxt(fn)[:,1], float)

def read_yres(fn):
    return asarray(loadtxt(fn)[:,2], float)

def read_ysd(fn):
    return asarray(loadtxt(fn)[:,3], float)

def read_rms(fn):
    with open(fn, 'rt') as fid:
        tp = re.findall('^#.*rms\s\(mm\).*', fid.read(), re.M)
        assert len(tp)==1
        return float(tp[0].split()[-1])

def read_std(fn):
    with open(fn, 'rt') as fid:
        tp = re.findall('.*std error.*', fid.read())
        assert len(tp)==1
        return float(tp[0].split()[-1])

def read_sea(fn):
    with open(fn, 'rt') as fid:
        tp = re.findall('^#\s*seasonal magnitude.*', fid.read(), re.M)
        if len(tp) == 0:
            return nan
        if len(tp) == 1:
            return float(tp[0].split(':')[1])

def read_semi(fn):
    with open(fn, 'rt') as fid:
        tp = re.findall('^#\s*semi-seasonal magnitude.*', fid.read(), re.M)
        if len(tp) == 0:
            return nan
        if len(tp) == 1:
            return float(tp[0].split(':')[1])

def read_linsec(fn):
    with open(fn,'rt') as fid:
        outs = re.findall('.*linear sec.*',fid.read())
    res = []
    for out in outs:            
        linsec = out.split(':')[1].split()
        assert len(linsec)==2
        t1 = linsec[0]
        t2 = linsec[1]
        if t1 == '-inf':
            t1 = -9999
        if t2 == 'inf':
            t2 = 9999999999
        res.append((int(t1),int(t2)))
    return res

def read_outlier(fn):
    with open(fn,'rt') as fid:
        out = re.findall('.*outliers.*',fid.read())[0]

    outlier = out.split(":")[1].split()
    return [int(ii) for ii in outlier]

def read_jumps(fn):
    with open(fn,'rt') as fid:
        out = re.findall('^#.*jump:.*',fid.read(),re.M)
    return [int(ii.split(':')[1]) for ii in out]

def read_vel(file):
    with open(file) as fid:
        tp = re.findall('^#.*velocity\s\(mm/yr\):.*',fid.read(), re.M)
    assert len(tp) == 1
    return float(tp[0].split(':')[1])

def read_vel_sd(file):
    with open(file) as fid:
        tp = re.findall('^#.*velocity\ssd\s\(mm/yr\):.*',fid.read(), re.M)
    assert len(tp) == 1
    return float(tp[0].split(':')[1])    

def gen_vel_and_vsd_file(lres_dir, sites, output_file):
    assert os.path.exists(lres_dir)
    pos_dic = get_pos_dic()
    with open(output_file, 'w') as fid:
        fid.write('# site  lon  lat  e(mm/yr)  n   u   esd   nsd   usd\n')
        
        for site in sites:
            lon = pos_dic[site.encode()][0]
            lat = pos_dic[site.encode()][1]
            fid.write('%s  %9f  %9f  '%(site, lon, lat))
            for cmpt in 'e','n','u':
                vel = read_vel(os.path.join(lres_dir,'%s.%s.lres'%(site,cmpt)))
                fid.write('%11f '%(vel))
            for cmpt in 'e','n','u':
                velsd = read_vel_sd(os.path.join(lres_dir,'%s.%s.lres'%(site,cmpt)))
                fid.write('%11f '%velsd)
            fid.write('\n')
