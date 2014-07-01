from os.path import join

import h5py
from numpy import linspace, meshgrid, asarray, loadtxt, nditer, inf

from .transform import FaultCoordinatesTransformation

class SubfaultsMeshes(FaultCoordinatesTransformation):
    def __init__(self):
        super().__init__()
        self.num_subflt_along_strike = None
        self.num_subflt_along_dip = None
        self.depth_limit = None
        
    def _init(self):
        self.y_f = linspace(1e-4, self.flt_dim_strike, self.num_subflt_along_strike)
        self.subflt_dim_strike = self.y_f[1] - self.y_f[0]

        # Grid point along length of fault in fault coordinates
        xf_lim = self.get_xf_by_dep_scalar(self.depth_limit)
        
        self.x_f = linspace(1e-4, xf_lim, self.num_subflt_along_dip)
        
        self.subflt_dim_dip = self.x_f[1] - self.x_f[0]

        self.xx_f, self.yy_f = meshgrid(self.x_f, self.y_f)

        self.LLons, self.LLats = self.fault2geo(self.xx_f, self.yy_f)

        self.xx_g, self.yy_g = self.fault2ground(self.xx_f, self.yy_f)

        self.ddeps = self.get_dep(self.xx_f)
        self.ddips = self.get_dip(self.xx_f)
        self.shear = self.get_shear(self.ddeps)

    def save_fault_file(self, fn):
        self._init()
        with h5py.File(fn) as fid:
            fid['num_subflt_along_strike'] = self.num_subflt_along_strike
            fid['num_subflt_along_dip'] = self.num_subflt_along_dip

            fid['flt_strike'] = self.flt_strike
            fid['flt_strike'].attrs['unit'] = 'degree'
            
            fid['subflt_sz_dip'] = self.subflt_dim_dip
            fid['subflt_sz_dip'].attrs['unit'] = 'km'
            
            fid['subflt_sz_strike'] = self.subflt_dim_strike
            fid['subflt_sz_strike'].attrs['unit'] = 'km'

            fid['flt_sz_dip'] = self.flt_dim_dip
            fid['flt_sz_dip'].attrs['unit'] = 'km'

            fid['flt_sz_strike'] = self.flt_dim_strike
            fid['flt_sz_strike'].attrs['unit'] = 'km'

            fid['depth_limit'] = self.depth_limit
            fid['depth_limit'].attrs['unit'] = 'km'
            
            fid['meshes/xx_f'] = self.xx_f.T
            fid['meshes/xx_f'].attrs['unit'] = 'km'
            
            fid['meshes/yy_f'] = self.yy_f.T
            fid['meshes/yy_f'].attrs['unit'] = 'km'
            
            fid['meshes/LLons'] = self.LLons.T
            fid['meshes/LLats'] = self.LLats.T

            fid['meshes/xx_g'] = self.xx_g.T
            fid['meshes/xx_g'].attrs['unit'] = 'km'
            
            fid['meshes/yy_g'] = self.yy_g.T
            fid['meshes/yy_g'].attrs['unit'] = 'km'

            fid['meshes/ddeps'] = self.ddeps.T
            fid['meshes/ddeps'].attrs['unit'] = 'km'
            
            fid['meshes/ddips'] = self.ddips.T
            fid['meshes/ddips'].attrs['unit'] = 'degree'

            fid['meshes/shear'] = self.shear.T
            fid['meshes/shear'].attrs['unit']='Pa.s'
            
        
        
        

    
        

