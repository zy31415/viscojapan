from os.path import join, exists
from os import makedirs

import numpy as np
from numpy import size
import h5py

from ..fault_model.fault_file_io import FaultFileReader

__all__=['gen_subflts_input',
         'gen_subflts_input_point_source']

def gen_subflts_input(fault_file, out_dir, rake, slip = None):
    if not exists(out_dir):
        makedirs(out_dir)

    rake = rake

    fid = FaultFileReader(fault_file)
    LLons=fid.LLons
    LLats=fid.LLats
    ddeps=fid.ddeps
    ddips=fid.ddips
    sflen=fid.subflt_sz_strike
    stk=fid.flt_strike
    
    udep = ddeps[:-1,:-1].flatten()
    ldep = ddeps[1:,:-1].flatten()
    dip = ddips[1:,1:].flatten()

    lat = LLats[1:,1:].flatten()
    lon = LLons[1:,1:].flatten()

    if slip is None:
        slip = np.ones_like(udep)
    else:
        slip = np.asarray(slip, float).flatten()

    no=size(udep)

    assert size(ldep)==no
    assert size(dip)==no
    assert size(lat)==no
    assert size(lon)==no
    assert len(slip) == no

    n=0
    for ui,li,di,lati,loni, si in zip(udep,ldep,dip,lat,lon, slip):
        with open(join(out_dir, 'flt_%04d'%n),'wt') as fid:
            fid.write('%f %f %f\n'%(li,ui,di))
            fid.write('1\n')
            fid.write('%f %f %f %.3f %.3f %f\n'%\
                      (lati,loni,sflen,stk,rake,si))
        print(n)
        n+=1

def gen_subflts_input_point_source(fault_file, out_dir, rake=90.):
    if not exists(out_dir):
        makedirs(out_dir)

    rake = rake

    fid = FaultFileReader(fault_file)
    LLons=fid.LLons
    LLats=fid.LLats
    ddeps=fid.ddeps
    ddips=fid.ddips
    sflen=fid.subflt_sz_strike
    sfwid = fid.subflt_sz_dip
    stk=fid.flt_strike

    dip = ddips[1:,1:].flatten()
    
    ps_wid = 0.2             
    slip = sfwid/ps_wid
    udep = ddeps[:-1,:-1].flatten()
    ldep = udep + ps_wid * np.sin(dip * np.pi / 180.)
    
    lat = LLats[1:,1:].flatten()
    lon = LLons[1:,1:].flatten()

    no=size(udep)

    assert size(ldep)==no
    assert size(dip)==no
    assert size(lat)==no
    assert size(lon)==no

    n=0
    for ui,li,di,lati,loni in zip(udep,ldep,dip,lat,lon):
        with open(join(out_dir, 'flt_%04d'%n),'wt') as fid:
            fid.write('%f %f %f\n'%(li,ui,di))
            fid.write('1\n')
            fid.write('%f %f %f %.3f %.3f %f\n'%\
                      (lati,loni,sflen,stk,rake,slip))
        print(n)
        n+=1


