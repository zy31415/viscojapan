import re
from os.path import basename

from numpy import nan

def read_rms(fn):
    with open(fn, 'rt') as fid:
        tp = re.findall('^#.*RMS\s\(mm\).*', fid.read(), re.M)
        assert len(tp)==1
        tp = tp[0].split(':')[1].split()
        assert (len(tp)==3) or (len(tp)==2)        
        return [float(ii) for ii in tp]

def collect_value(files, reader):
    val_dic = {}
    for file in files:
        tp = basename(file).split('.')
        site = tp[0]
        val = reader(file)
        val_dic[site] = {}
        val_dic[site]['e'] = val[0]
        val_dic[site]['n'] = val[1]
        
        if len(val)==2:            
            val_dic[site]['u'] = nan            
        elif len(val)==3:
            val_dic[site]['u'] = val[2]
        else:
            raise ValueError('')
    return val_dic
