import warnings

from numpy import asarray, pi, cos, sin, zeros_like
from pyproj import Proj
try:
    from pylab import plt
except Exception:
    pass

from ..utils import my_vectorize, _find_section

__all__=['plot_fault_framework','FaultFramework']

def plot_fault_framework(fault_framework):
    fm = fault_framework
    plt.plot(fm.Y_PC, fm.DEP, '-o')
    plt.axis('equal')
    plt.axhline(0, color='black')
    plt.gca().set_yticks(fm.DEP)
    plt.gca().set_xticks(fm.Y_PC)
    plt.grid('on')
    plt.title('Ground x versus depth')
    plt.xlabel('Ground X (km)')
    plt.ylabel('depth (km)')

    for xi, yi, dip in zip(fm.Y_PC, fm.DEP, fm.DIP_D):
        plt.text(xi, yi, 'dip = %.1f'%dip)

    plt.gca().invert_yaxis()
        
class FaultFramework(object):
    ''' Three coordinates:
Fault Plane Coordinates (FC)
    (xfc, yfc)
    xfc - along strike
    yfc - along dip
    
Ground Projection Coordinates (PC)
    (xgc, ypc)
    
Geographic Coordinates (GC)
    (lon,lat)
    
Explaination see research notes on July 01, 2014.
07/01/2014
'''
    def __init__(self, control_points):

        self.control_points = control_points
        
        self._fault_origin()
        self._fault_dimension()
        self._fault_orientation()
        self._hinge_coordinates()
        self._hinge_dep()

    def _fault_origin(self):        
        # Lon and Lat of a fault corner, which is the origianl point
        #  in fault coordinates.
        self.B0 = self.control_points.B0

    def _fault_dimension(self):
        # Total fault width
        self.FLT_SZ_DIP = self.control_points.FLT_SZ_DIP 

    def _fault_orientation(self):
        # Subfaults dips in degree.
        self.DIP_D = asarray(self.control_points.DIP_D, float)
        # Subfaults dips in arcs.
        self.DIP = self.DIP_D*pi/180.
        
        # Fault STRIKE    
        self.STRIKE = self.control_points.STRIKE

    def _hinge_coordinates(self):        
        #                dY_PC[0]      dY_PC[1]
        # Ground: Y_PC[0]--------Y_PC[1]-------Y_PC[2]---...
        #
        #               dY_FC[0]       dY_FC[1]
        # Fault:  Y_FC[0]--------Y_FC[1]-------Y_FC[2]---...
        #
        # Y_PC is x coordiantes of ground nodal points in the ground xy coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        # Note Y_PC has order!
        self.Y_PC = asarray(self.control_points.Y_PC, float)
        self.dY_PC = self.Y_PC[1:] - self.Y_PC[0:-1]

        # Y_FC is x coordinates of nodal points in fault coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        self.Y_FC= asarray(self.control_points.Y_FC, float)
        self.dY_FC= self.Y_FC[1:] - self.Y_FC[0:-1]

    def _hinge_dep(self):
        # initial depth of the upper edge of the shallowest subfaults.
        self.DEP0 = self.control_points.DEP0 

        # DEP is the depth of the fault hinges
        DEP = [self.DEP0]
        for seg,dip in zip(self.dY_FC, self.DIP):
            _y1 = DEP[-1] + seg*sin(dip)
            DEP.append(_y1)
        self.DEP = DEP
            
    def _get_dip_scalar(self, yfc):
        nth = _find_section(self.Y_FC, yfc)
        dip = self.DIP_D[nth-1]
        return dip      
    
    def get_dip(self, yfc):
        return my_vectorize(self._get_dip_scalar, yfc)

    def _get_dep_scalar(self, yfc):
        nth = _find_section(self.Y_FC, yfc)
        
        xf1 = self.Y_FC[nth-1]
        xf2 = self.Y_FC[nth]
        dep1 = self.DEP[nth-1]
        dep2 = self.DEP[nth]

        dep = (dep2-dep1)/(xf2-xf1)*(yfc-xf1) + dep1
        return dep

    def get_dep(self, yfc):
        return my_vectorize(self._get_dep_scalar, yfc)

    def get_yfc_by_dep_scalar(self, dep):
        nth = _find_section(self.DEP, dep)        
        d1 = self.DEP[nth-1]
        d2 = self.DEP[nth]
        xf1 = self.Y_FC[nth-1]
        xf2 = self.Y_FC[nth]

        yfc = (xf2-xf1)/(d2-d1)*(dep-d1) + xf1
        return yfc

    def _yfc_to_ypc_scalar(self, yfc):
        nth = _find_section(self.Y_FC, yfc)
        
        res = self.Y_PC[nth-1] + (yfc - self.Y_FC[nth-1])*cos(self.DIP[nth-1])
        return res

    def yfc_to_ypc(self, yfc):
        yfc = asarray(yfc, float)
        return my_vectorize(self._yfc_to_ypc_scalar, yfc)

    def _ypc_to_yfc_scalar(self, ypc):
        nth = _find_section(self.Y_PC, ypc)
        
        res =  self.Y_FC[nth-1] + (ypc-self.Y_PC[nth-1])/cos(self.DIP[nth-1])
        return res

    def ypc_to_yfc(self, ypc):
        return my_vectorize(self._ypc_to_yfc_scalar, ypc)



        
        
        

