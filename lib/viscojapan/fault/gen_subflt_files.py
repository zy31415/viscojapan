from os.path import join, exists
from os import makedirs

from numpy import size

import h5py

def gen_subflts_files(fault_file, out_dir):
    if not exists(out_dir):
        makedirs(out_dir)
    with h5py.File(fault_file) as fid:        
        LLons=fid['meshes/LLons'][...]
        LLats=fid['meshes/LLats'][...]
        ddeps=fid['meshes/ddeps'][...]
        ddips=fid['meshes/ddips'][...]
        sflen=fid['subflt_sz_strike'][...]
        stk=fid['flt_strike'][...]
    
    udep = -ddeps[:-1,:-1].flatten()
    ldep = -ddeps[1:,:-1].flatten()
    dip = ddips[1:,1:].flatten()

    lat = LLats[1:,1:].flatten()
    lon = LLons[1:,1:].flatten()

    no=size(udep)

    assert size(ldep)==no
    assert size(dip)==no
    assert size(lat)==no
    assert size(lon)==no

    n=0
    for ui,li,di,lati,loni in zip(udep,ldep,dip,lat,lon):
        if li > 60:
            raise ValueError()
        with open(join(out_dir, 'flt_%04d'%n),'wt') as fid:
            fid.write('%f %f %f\n'%(li,ui,di))
            fid.write('1\n')
            fid.write('%f %f %f %f %f %f\n'%\
                      (lati,loni,sflen,stk,90.,1.))
        print(n)
        n+=1

    
