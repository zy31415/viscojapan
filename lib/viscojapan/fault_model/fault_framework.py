import warnings

from numpy import asarray, pi, cos, sin, zeros_like
from pyproj import Proj

from ..utils import my_vectorize, _find_section

        
class FaultFramework(object):
    ''' Three coordinates:
Fault Plane Coordinates (FC)
    (xfc, yfc)
    xfc - along strike
    yfc - along dip
Ground Projection Coordinates (GC)
    (xgc, ygc)
Geographic Coordinates (GC)
    (lon,lat)
Explaination see research notes on July 01, 2014.
07/01/2014
'''
    def __init__(self):
        self._fault_origin()
        self._fault_dimension()
        self._fault_orientation()
        self._hinge_coordinates()
        self._hinge_dep()

    def _fault_origin(self):        
        # Lon and Lat of a fault corner, which is the origianl point
        #  in fault coordinates.
        self.B0 = (144.697756238647, 40.25451048457508)

    def _fault_dimension(self):
        # Total fault width
        self.FLT_SZ_DIP = 425.

        # Total fault length
        self.FLT_SZ_STRIKE = 700.

    def _fault_orientation(self):
        # Subfaults dips in degree.
        self.DIP_D = asarray([10.,14.,22.,28.])
        # Subfaults dips in arcs.
        self.DIP = self.DIP_D*pi/180.
        
        # Fault STRIKE    
        self.STRIKE = 195.

    def _hinge_coordinates(self):        
        #                dY_GC[0]      dY_GC[1]
        # Ground: Y_GC[0]--------Y_GC[1]-------Y_GC[2]---...
        #
        #               dY_FC[0]       dY_FC[1]
        # Fault:  Y_FC[0]--------Y_FC[1]-------Y_FC[2]---...
        #
        # Y_GC is x coordiantes of ground nodal points in the ground xy coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        # Note Y_GC has order!
        self.Y_GC = asarray([0,98.480775301220802,171.25295477192054,
                       217.61214750025991, 394.20166607204533])
        self.dY_GC = self.Y_GC[1:] - self.Y_GC[0:-1]

        # Y_FC is x coordinates of nodal points in fault coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        self.Y_FC=[0,100.,175.,225.,425.]
        self.dY_FC=[100.,75.,50.,200]

    def _hinge_dep(self):
        # initial depth of the upper edge of the shallowest subfaults.
        self.DEP0 = 3.

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
        

    def _yfc_to_ygc_scalar(self, yfc):
        nth = _find_section(self.Y_FC, yfc)
        
        res = self.Y_GC[nth-1] + (yfc - self.Y_FC[nth-1])*cos(self.DIP[nth-1])
        return res

    def yfc_to_ygc(self, yfc):
        yfc = asarray(yfc, float)
        return my_vectorize(self._yfc_to_ygc_scalar, yfc)

    def _ygc_to_yfc_scalar(self, ygc):
        nth = _find_section(self.Y_GC, ygc)
        
        res =  self.Y_FC[nth-1] + (ygc-self.Y_GC[nth-1])/cos(self.DIP[nth-1])
        return res

    def ygc_to_yfc(self, ygc):
        return my_vectorize(self._ygc_to_yfc_scalar, ygc)
        
        

