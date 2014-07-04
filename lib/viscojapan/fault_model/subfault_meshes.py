from os.path import join

import h5py
from numpy import linspace, meshgrid, asarray, loadtxt, nditer, inf

from .transform import FaultCoordinatesTransformation
from ..utils import overrides, kw_init


def accumulate_to_form_array(step_size, limit):
    assert step_size > 0.
    assert limit > 0.
    s = [0.]
    si = 0.
    while si <= limit:
        si += step_size
        s.append(si)

    return asarray(s[0:-1], float)


class SubfaultsMeshes(FaultCoordinatesTransformation):
    def __init__(self):
        super().__init__()
        self.x_f = None
        self.y_f = None
        
    def _init(self):
        self.num_subflt_along_strike = len(self.x_f)-1
        self.num_subflt_along_dip =  len(self.y_f)-1

        self.subflt_sz_strike = self.x_f[1] - self.x_f[0]
        self.subflt_sz_dip = self.y_f[1] - self.y_f[0]

        self.flt_sz_strike = self.x_f[-1] - self.x_f[0]
        self.flt_sz_dip = self.y_f[-1] - self.y_f[0]
        
        self.xx_f, self.yy_f = meshgrid(self.x_f, self.y_f)

        self.LLons, self.LLats = self.fault2geo(self.xx_f, self.yy_f)

        self.xx_p, self.yy_p = self.fault2ground(self.xx_f, self.yy_f)

        self.ddeps = self.get_dep(self.yy_f)
        self.ddips = self.get_dip(self.yy_f)

        self.depth_bottom = self.get_dep(self.y_f[-1])

    def save_fault_file(self, fn):
        self._init()
        with h5py.File(fn) as fid:
            fid['num_subflt_along_strike'] = self.num_subflt_along_strike
            fid['num_subflt_along_dip'] = self.num_subflt_along_dip

            fid['flt_strike'] = self.STRIKE
            fid['flt_strike'].attrs['unit'] = 'degree'
            
            fid['subflt_sz_dip'] = self.subflt_sz_dip
            fid['subflt_sz_dip'].attrs['unit'] = 'km'
            
            fid['subflt_sz_strike'] = self.subflt_sz_strike
            fid['subflt_sz_strike'].attrs['unit'] = 'km'

            fid['flt_sz_dip'] = self.flt_sz_dip
            fid['flt_sz_dip'].attrs['unit'] = 'km'

            fid['flt_sz_strike'] = self.flt_sz_strike
            fid['flt_sz_strike'].attrs['unit'] = 'km'

            fid['depth_top'] = self.DEP[0]
            fid['depth_top'].attrs['unit'] = 'km'
            
            fid['depth_bottom'] = self.depth_bottom
            fid['depth_bottom'].attrs['unit'] = 'km'

            fid['x_f'] = self.x_f
            fid['x_f'].attrs['unit'] = 'km'

            fid['y_f'] = self.y_f
            fid['y_f'].attrs['unit'] = 'km'            
            
            fid['meshes/xx_f'] = self.xx_f
            fid['meshes/xx_f'].attrs['unit'] = 'km'
            
            fid['meshes/yy_f'] = self.yy_f
            fid['meshes/yy_f'].attrs['unit'] = 'km'
            
            fid['meshes/LLons'] = self.LLons
            fid['meshes/LLats'] = self.LLats

            fid['meshes/xx_p'] = self.xx_p
            fid['meshes/xx_p'].attrs['unit'] = 'km'
            
            fid['meshes/yy_p'] = self.yy_p
            fid['meshes/yy_p'].attrs['unit'] = 'km'

            fid['meshes/ddeps'] = self.ddeps
            fid['meshes/ddeps'].attrs['unit'] = 'km'
            
            fid['meshes/ddips'] = self.ddips
            fid['meshes/ddips'].attrs['unit'] = 'degree'
    
            
class SubfaultsMeshesByLength(SubfaultsMeshes):
    def __init__(self, **kwargs):
        super().__init__()
        self.subflt_sz_dip = None
        self.depth_bottom_limit = None

        self.flt_sz_strike_limit = 700. # km
        self.subflt_sz_strike = None

        kw_init(self, kwargs)

    def _gen_y_f(self):
        y_f_limit = self.get_yfc_by_dep_scalar(self.depth_bottom_limit)
        self.y_f = accumulate_to_form_array(self.subflt_sz_dip, y_f_limit)

    def _gen_x_f(self):
        self.x_f = accumulate_to_form_array(self.subflt_sz_strike,
                                            self.flt_sz_strike_limit)            
    @overrides(SubfaultsMeshes)
    def _init(self):
        self._gen_x_f()
        self._gen_y_f()
        super()._init()


class SubfaultsMeshesByNumber(SubfaultsMeshes):
    def __init__(self):
        super().__init__()
        self.num_subflt_along_strike = None
        self.flt_sz_strike = 700. # km
        
        self.num_subflt_along_dip = None        
        self.depth_bottom_limit = None

    def _gen_y_f(self):
        y_f_limit = self.get_yfc_by_dep_scalar(self.depth_bottom_limit)
        self.y_f = linspace(0, y_f_limit, self.num_subflt_along_dip+1)
       
    def _gen_x_f(self):
        self.x_f = linspace(0, self.flt_sz_strike,
                            self.num_subflt_along_strike+1)
        
    @overrides(SubfaultsMeshes)
    def _init(self):
        self._gen_x_f()
        self._gen_y_f()
        super()._init()

        

