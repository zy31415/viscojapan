from os.path import exists

import h5py

from ..utils import _assert_positive_integer

class FaultFileIO(object):
    def __init__(self, fault_file):
        self.fault_file = fault_file

    def read(self):
        '''Readonly, file must exist'''
        assert exists(self.fault_file), \
               'File %s does not exist!'%self.fault_file
        fid = h5py.File(self.fault_file, 'r')
        return fid

    def append(self):
        '''Read/write if exists, create otherwise (default)'''
        fid = h5py.File(self.fault_file, 'r')
        return fid

    @property
    def num_subflt_along_strike(self):
        with self.read() as fid:
            res = fid['num_subflt_along_strike'][...]
        return int(res)

    @num_subflt_along_strike.setter
    def num_subflt_along_strike(self, val):
        _assert_positive_integer(val)
        with self.append() as fid:
            fid['num_subflt_along_strike'] = val

    @property
    def num_subflt_along_dip(self):
        with self.read() as fid:
            res = fid['num_subflt_along_dip'][...]
        return int(res)

    @num_subflt_along_dip.setter
    def num_subflt_along_dip(self, val):
        _assert_positive_integer(val)
        with self.append() as fid:
            fid['num_subflt_along_strike'] = val

    @property
    def LLons(self):
        with self.read() as fid:
            res = fid['meshes/LLons'][...]
        return res

    @property
    def LLats(self):
        with self.read() as fid:
            res = fid['meshes/LLats'][...]
        return res

    @property
    def ddeps(self):
        with self.read() as fid:
            res = fid['meshes/ddeps'][...]
        return res

    @property
    def ddips(self):
        with self.read() as fid:
            res = fid['meshes/ddips'][...]
        return res

    @property
    def subflt_sz_strike(self):
        with self.read() as fid:
            res = fid['subflt_sz_strike'][...]
        return float(res)

    @property
    def subflt_sz_dip(self):
        with self.read() as fid:
            res = fid['subflt_sz_dip'][...]
        return float(res)

    @property
    def flt_strike(self):
        with self.read() as fid:
            assert 'flt_strike' in fid
            res = fid['flt_strike'][...]
        return float(res)

    @property
    def depth_bottom(self):
        with self.read() as fid:
            assert 'depth_bottom' in fid
            res = fid['depth_bottom'][...]
        return float(res)

    @property
    def depth_top(self):
        with self.read() as fid:
            assert 'depth_top' in fid
            res = fid['depth_top'][...]
        return float(res)
    

    

    
            
            

    

    
        
