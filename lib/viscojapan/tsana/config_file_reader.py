''' Functions in this file read config files for time series modeling.

'''
import re
import warnings
from os.path import join

import numpy as np
from numpy import inf

from date_conversion import asmjd,asdtype

from .utils import if_in_tcuts_boundary

__all__ = ['get_sites_according_to_postmodel']

def get_sites_according_to_postmodel(config_file_postmodel, cmpt_code, post_model) -> list:
    tp = np.loadtxt(config_file_postmodel, '4a, i, 5a')
    sites = []
    for ii in tp:
        site = ii[0]
        cmpt_code_ = int(ii[1])
        post_model_ = ii[2].decode()
        assert isinstance(cmpt_code_, int), \
               'cmpt_code %d is wrong.'%cmpt_code_
        assert post_model_ in ('EXP','2EXPs'), 'post_model code %s is wrong.'%post_model_
        
        if (cmpt_code_ == cmpt_code) and (post_model_ == post_model):
            sites.append(site)
    return sites


class ConfigFileReader(object):
    ''' This class provides functions to read model config file.
'''
    def __init__(self, dir_config_files):
        self.dir_config_files = dir_config_files
        self.file_jumps = join(self.dir_config_files, 'jumps')
        self.file_linsec = join(self.dir_config_files, 'linsec')
        self.file_postmodel = join(self.dir_config_files, 'postmodel')
        self.file_postsec = join(self.dir_config_files, 'postsec')
        self.file_sea = join(self.dir_config_files, 'sea')
        self.file_outlier = join(self.dir_config_files, 'outlier')

    def get_jumps(self,site,tcuts=[(-inf,inf)]):
        with open(self.file_jumps) as fid:
            jumps = re.findall('^\s*%s.*'%site,fid.read(),re.M)
        outs = []
        for jump in jumps:
            spl=jump.split()
            assert len(spl) == 2 or len(spl) == 3, \
                   "Wrong item. Check jumps file."
            site=spl[0]
            t=asmjd(spl[1])
            if len(spl)==3:
                cause=spl[2]
            else:
                cause=None

            if if_in_tcuts_boundary(t,tcuts):
                outs.append(t)
        return outs

    def _get_sea_code(self,site):
        ''' Read sea file and return model code of seasonal part.
'''
        with open(self.file_sea) as fid:
            tp=re.findall('^\s*%s.*'%site,fid.read(),re.M)
            assert len(tp) < 2, 'Check file.'
            if len(tp)==0:
                warnings.warn(
                    "Site %s Not found in config file %s. Default value 0b11 are used."%\
                    (site,self.file_sea))
                return 0b11
        code = int(tp[0].split()[1])
        return code        

    def if_sea(self, site):
        ''' Whether seasonal component should be estimated?
    '''
        code = self._get_sea_code(site)
        if code == 0b10 or code == 0b11:
            return True
        return False

    def if_semi(self,site):
        ''' Whether semi-seasonal component should be estimated?
    '''
        code = self._get_sea_code(site)
        if code == 0b01 or code == 0b11:
            return True
        return False

    @staticmethod        
    def _get_sec(file_sec, site, dtype='mjd'):
        ''' Read time sections from time section file.
    '''
        with open(file_sec) as fid:
            linsecs=re.findall('^\s*%s.*'%site,fid.read(),re.M)
        out=[]
        for li in linsecs:
            tp=li.split()
            t1=tp[1]
            t2=tp[2]
            if t1.upper()=='-INF':
                t1=-inf
            else:
                t1=asdtype(t1,dtype)
            if t2.upper()=='INF' or t2.upper()=='+INF':
                t2=inf
            else:
                t2=asdtype(t2,dtype)
            out.append((t1,t2))
        return out

    def get_postsec(self,site,dtype='mjd'):
        res=ConfigFileReader._get_sec(self.file_postsec,site,dtype)
        if res==[]:
            warnings.warn("Not found in config file. Default value are used.",)
            res=[(asdtype('11MAR11',dtype),+inf)]
        return res
        

    def get_linsec(self,site,dtype='mjd'):
        ''' Read linsec from f_linsec.
    '''
        res=ConfigFileReader._get_sec(self.file_linsec,site,dtype)
        if res==[]:
            warnings.warn("Not found in config file. Default value are used.",)
            res=[(-inf,asdtype('11MAR11',dtype))]
        return res

    def get_post_model(self,site):
        ''' Return
(1) Which components are used in modeling, indicated by 3 digits binary.
(2) Postseismic time series model.
'''
        with open(self.file_postmodel) as fid:
            out=re.findall('^\s*%s.*'%site,fid.read(),re.M)
        assert not (len(out)>1), "More than one entries."
        assert len(out)!=0, "Not found in the config file."
        
        out=out[0].split()
        assert len(out)==3, "Wrong entry"
        
        return int(out[1]),out[2]

    def get_outlier_sd(self,site):
        with open(self.file_outlier) as fid:
            out = re.findall('^\s*%s.*'%site, fid.read(), re.M)
        if len(out)==0:
            print("Not found in outlier file. Use default model.")
            return None
        assert len(out)==1, 'More than one entry.'
        entry = out[0]
        entry = entry.split()
        site = entry[0]
        st = float(entry[1])
        return st



if __name__=='__main__':
    reader=ConfigFileReader()
    site='J550'
    print(reader.get_jumps(site,[(55555,55632)]))
    print(reader.if_sea(site))
    print(reader.if_semi(site))
    print(reader.get_linsec(site))
    print(reader.get_postsec(site))
    print(reader.get_post_model(site))
