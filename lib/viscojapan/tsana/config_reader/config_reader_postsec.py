import warnings
from os.path import exists
import re

import numpy as np

from date_conversion import asmjd,asdtype

from .utils import get_sec
from .share import config_file_postsec, config_file_jumps,\
     config_file_post_model, config_file_post_cc
from ..utils import if_in_tcuts_boundary

__all__ = ['ConfigReaderPostSec', 'ConfigReaderJumps', 'ConfigReaderPostModel',
           'ConfigReaderPostCC']

class _ConfigReader(object):
    def __init__(self, config_file):
        self.config_file = config_file        
        assert exists(self.config_file), "Config. file %s doesn't exist"%\
               self.config_file

class ConfigReaderPostSec(_ConfigReader):
    def __init__(self, config_file = None):
        if config_file is None:
            config_file = config_file_postsec
        super().__init__(config_file)
        
    def read(self, site, dtype='mjd'):
        res = get_sec(self.config_file,site,dtype)
        if res==[]:
            warnings.warn("Not found in config file. Default value are used.",)
            res=[(asdtype('11MAR11',dtype),+np.inf)]
        return res

class ConfigReaderJumps(_ConfigReader):
    def __init__(self, config_file = None):
        if config_file is None:
            config_file = config_file_jumps
        super().__init__(config_file)
        
    def read(self, site, tcuts=[(-np.inf, np.inf)]):
        with open(self.config_file) as fid:
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
        
class ConfigReaderPostModel(_ConfigReader):
    def __init__(self, config_file = None):
        if config_file is None:
            config_file = config_file_post_model
        super().__init__(config_file)

        self._dict = { ii[0].decode():ii[1].decode()
                       for ii in np.loadtxt(self.config_file, '4a,5a', usecols=(0,1))
                       }
        
    def read(self, site):
        return self._dict[site]

class ConfigReaderPostCC(_ConfigReader):
    def __init__(self, config_file = None):
        if config_file is None:
            config_file = config_file_post_cc
        super().__init__(config_file)

        self._dict = { ii[0].decode():ii[1]
                       for ii in np.loadtxt(self.config_file, '4a,i', usecols=(0,1))
                       }
        
    def read(self, site):
        return self._dict[site]

    def get_cmpts(self, site):
        if self.component_code == 6:
            self.components ='en'
        elif self.component_code == 7:
            self.components = 'enu'
        else:
            raise ValueError()
        
