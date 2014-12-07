from numpy import inf
import re

from .share import raw_file_He33km, raw_file_He40km, \
     raw_file_He45km, raw_file_He50km, \
     raw_file_He55km, raw_file_pollitz_He63km

__all__ = ['GenerateEarthModelFile']

class GenerateEarthModelFile(object):
    def __init__(self,
                 raw_file,
                 fault_bottom_depth,
                 visK = inf,
                 visM = inf,                 
                 ):
        self.raw_file = raw_file
        self.fault_bottom_depth = fault_bottom_depth
        self.visK = visK
        self.visM = visM

    def _check_num_of_layers(self, txt):
        ln = txt.strip().split('\n')
        n = int(ln[0].split()[0])
        assert len(ln) == n+1, '%d != %d'%(len(ln), n+1)

    def gen_earthmodel_file(self):
        if self.visK == inf:
            self.visK=1e29
        if self.visM == inf:
            self.visM=1e29

        DEPFAC = self.fault_bottom_depth/28.
        with open(self.raw_file,'rt') as fid:
            txt=fid.read()
            txt=re.sub('\\bK{12}\\b','%12E'%(self.visK/1e18),txt)
            txt=re.sub('\\bM{12}\\b','%12E'%(self.visM/1e18),txt)
            txt=re.sub('\\bD{4}\\b','%.3f'%DEPFAC, txt)

        self._check_num_of_layers(txt)        
        return txt

    def save(self, fn):
        with open(fn,'wt') as fid:
            fid.write(self.gen_earthmodel_file())
