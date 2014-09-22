from pylab import *

from ._DC3D import dc3d0 as DC3D0
from ._DC3D import dc3d as DC3D

__all__=['dc3d']

class dc3d:
    ''' Wrapper class of Okada routine.
Initialization:

Material properties:
alpha = (lambda+mu)/(lambda+2*mu)
        default: 2/3.

Fault geometry:
flt_dep
        

'''
    def __init__(self):
        # material properties
        # alpha=(lambda+mu)/(lambda+2*mu)
        # Default value 2/3 implies lambda=mu, which is called 
        self.alpha=2./3.

        # fault geometry
        self.flt_dep=None
        self.x0=0.
        self.y0=0.

        self.dip=None
        self.stk=90.

        # source magnitude
        ## Left-lateral -  positive
        self.po_stk=0.
        self.po_dip=0.

        # Coordinate range in strike direction of the fault surface
        self.al1=None
        self.al2=None
        # Coordinate range in up-dip direction of the fault surface
        self.aw1=None
        self.aw2=None
        # Dislocation in strike-slip component
        self.disl1=0.
        # Dislocation in dip-slip component
        self.disl2=0.
        # Dislocation in tensile component
        self.disl3=0.
        
    def _dspl0(self,xi,yi):
        out=DC3D0(self.alpha,xi,yi,0.,
                  self.flt_dep,self.dip,
                  self.po_stk,self.po_dip,0.,0.)
        uxi=out[0]
        uyi=out[1]
        uzi=out[2]

        if out[-1]==0:
            return uxi,uyi,uzi
        
        if out[-1]==1:
            raise ValueError('Singular point!')

        if out[-1]==2:
            raise ValueError('Positive Z was given!')

    def _dspl(self,xi,yi):
        out=DC3D(self.alpha,xi,yi,0.,
                 self.flt_dep,self.dip,
                 self.al1,self.al2,self.aw1,self.aw2,
                 self.disl1,self.disl2,self.disl3)
        uxi=out[0]
        uyi=out[1]
        uzi=out[2]

        if out[-1]==0:
            return uxi,uyi,uzi
        
        if out[-1]==1:
            raise ValueError('Singular point!')

        if out[-1]==2:
            raise ValueError('Positive Z was given!')

    def rot_geo2flt(self,x,y):
        # rotation:
        a=self.stk-90.
        a=a*pi/180. # convert to rad before apply rotation.
        xp=cos(a)*x-sin(a)*y
        yp=sin(a)*x+cos(a)*y
        return xp,yp

    def rot_flt2geo(self,x,y):
        # rotation:
        a=self.stk-90.
        a=-a*pi/180. # convert to rad before apply rotation.
        xp=cos(a)*x-sin(a)*y
        yp=sin(a)*x+cos(a)*y     
        return xp,yp

    def dspl0(self,x,y):
        ''' Displacement at the surface.
Map the geo-coordinates into fault coordinates.
Then map the results backward into geo-coordinates.
'''
        x=asarray(x,'float')
        y=asarray(y,'float')
        assert x.shape==y.shape, "Inputs must be of the same shape."

        assert self.flt_dep>=0, "Falut depth should be positive."

        xp=x-self.x0
        yp=y-self.y0

        xp,yp=self.rot_geo2flt(xp,yp)       

        # Use ellipsis slicing syntax in Python:
        ux=zeros_like(xp)
        uy=zeros_like(xp)
        uz=zeros_like(xp)

        for uxi,uyi,uzi,xi,yi in zip(nditer(ux,op_flags=['readwrite']),
                                     nditer(uy,op_flags=['readwrite']),
                                     nditer(uz,op_flags=['readwrite']),
                                     nditer(xp),nditer(yp)):
            uxi[...],uyi[...],uzi[...]=self._dspl0(xi,yi)

        uxp,uyp=self.rot_flt2geo(ux,uy)       
        return uxp,uyp,uz

    def dspl(self,x,y):
        ''' Displacement at the surface.
Map the geo-coordinates into fault coordinates.
Then map the results backward into geo-coordinates.
'''
        x=asarray(x,'float')
        y=asarray(y,'float')
        assert x.shape==y.shape, "Inputs must be of the same shape."
        
        assert self.flt_dep>=0, "Falut depth should be positive."
        assert self.al2>self.al1, "al2 should be greater than al1"
        assert self.aw2>self.aw1, "aw2 should be greater than aw1"

        xp=x-self.x0
        yp=y-self.y0

        xp,yp=self.rot_geo2flt(xp,yp)       

        # Use ellipsis slicing syntax in Python:
        ux=zeros_like(xp)
        uy=zeros_like(xp)
        uz=zeros_like(xp)

        for uxi,uyi,uzi,xi,yi in zip(nditer(ux,op_flags=['readwrite']),
                                     nditer(uy,op_flags=['readwrite']),
                                     nditer(uz,op_flags=['readwrite']),
                                     nditer(xp),nditer(yp)):
            uxi[...],uyi[...],uzi[...]=self._dspl(xi,yi)

        uxp,uyp=self.rot_flt2geo(ux,uy)       
        return uxp,uyp,uz

if __name__=='__main__':
    d=dc3d()
    d.flt_dep=10.
    d.dip=30.
    d.po_dip=1.

    ux,uy,uz=d.dspl0([[1,2],[3,4]],[[1,2],[3,4]])
    print(ux)
    print(uy)
    print(uz)
