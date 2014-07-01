from numpy import asarray

class FaultFramework(object):
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
        self.flt_dim_dip = 425.

        # Total fault length
        self.flt_dim_strike = 700.

    def _fault_orientation(self):
        # Subfaults dips in degree.
        self.DIP_D = asarray([10.,14.,22.,28.])
        # Subfaults dips in arcs.
        self.DIP = DIP_D*pi/180.
        
        # Fault flt_strike    
        self.flt_strike = 195.

    def _hinge_coordinates(self):        
        #               dXG[0]      dXG[1]
        # Ground: XG[0]--------XG[1]-------XG[2]---...
        #
        #              dXF[0]       dXF[1]
        # Fault:  XF[0]--------XF[1]-------XF[2]---...
        #
        # XG is x coordiantes of ground nodal points in the ground xy coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        # Note XG has order!
        self.XG = asarray([0,98.480775301220802,171.25295477192054,
                       217.61214750025991, 394.20166607204533])
        self.dXG = XG[1:]-XG[0:-1]

        # XF is x coordinates of nodal points in fault coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        self.XF=[0,100.,175.,225.,425.]
        self.dXF=[100.,75.,50.,200]

    def _hinge_dep(self):
        # initial depth of the upper edge of the shallowest subfaults.
        self.DEP0 = -3.

        # DEP is the depth of the fault hinges
        DEP = [DEP0]
        for seg,dip in zip(self.dXF, self.DIP):
            _y1 = DEP[-1]-seg*sin(dip)
            DEP.append(_y1)
        self.DEP = DEP


class Transform(object):
    """ Coordinates transformations bewteen these three coordinates:
(1) Geo-coordinates expressed by (lon,lat)
(2) Ground coordinates expressed by (east,north) in km
(3) Fault coordinates in km
"""
    def __init__(self):
        global B0
        self.org_lon=B0[0]
        self.org_lat=B0[1]
        
        self.flt_strike=flt_strike


    def map_proj(self,x,y,inverse=False):
        p=Proj(proj='utm',zone=54,ellps='WGS84')
        return p(x,y,inverse=inverse)


    def rotate2strike(self,x,y,inverse=False):
        if inverse:
            alpha=self.flt_strike*pi/180
        else:
            alpha=-self.flt_strike*pi/180
        x1=cos(alpha)*x+sin(alpha)*y
        y1=-sin(alpha)*x+cos(alpha)*y
        return x1,y1

    def translate2epi(self,x,y,inverse=False):
        x0,y0=self.map_proj(self.org_lon,self.org_lat)
        if inverse:
            x+=x0
            y+=y0
        else:
            x-=x0
            y-=y0
        return x,y

    def tofault(self,x):
        global XG, XF, DIP
        x=asarray(x,dtype='float')
        _x=zeros_like(x)

        ch=(x<XG[0])|(x>XG[-1])
        _x[ch]=nan

        for nth in range(1,len(XG)):
            ch= (x>=XG[nth-1])&(x<=XG[nth])
            _x[ch]=XF[nth-1]+(x[ch]-XG[nth-1])/cos(DIP[nth-1])
        return _x

    ## Transform to ground coordinate.
    #
    def toground(self,x):
        global XG, XF, DIP
        x=asarray(x,dtype='float')
        _x=zeros_like(x)
        
        ch=(x<XF[0])|(x>XF[-1])
        _x[ch]=nan

        for nth in range(1,len(XG)):
            ch= (x>=XF[nth-1])&(x<=XF[nth])
            _x[ch]=XG[nth-1]+(x[ch]-XF[nth-1])*cos(DIP[nth-1])
        return _x
    
    def geo2xy(self,lon,lat):
        lon=asarray(lon,'float')
        lat=asarray(lat,'float')
        # map projection
        x,y=self.map_proj(lon,lat)

        # translate
        x,y=self.translate2epi(x,y)

        # dimension change
        x/=1000. # m->km
        y/=1000.

        return x,y

    def xy2geo(self,x,y):
        # dimension change
        x1=x*1000. # km->m
        y1=y*1000.

        # translate
        x,y=self.translate2epi(x,y,inverse=True)

        # map projection
        lon,lat=self.map_proj(x,y,inverse=True)
        return lon,lat

    def fault2geo(self,x,y):
        xp=self.toground(x)
        # dimension change
        x1=x*1000. # km->m
        y1=y*1000.

        # rotation
        x,y=self.rotate2strike(x1,y1,inverse=True)

        #translate
        x,y=self.translate2epi(x,y,inverse=True)

        # map projection
        lon,lat=self.map_proj(x,y,inverse=True)
        return lon,lat


class SubfaultMesh(object):
    def __init__(self):
        
    def get_dip(xf):
        out=zeros_like(xf)
        ch=(xf<XF[0])
        out[ch]=DIP_D[0]
        ch= (xf>XF[-1])
        out[ch]=DIP_D[-1]
        
        for x1,x2,dip in zip(XF[0:-1],XF[1:],DIP_D):
            ch= (xf>=x1) & (xf<=x2)
            out[ch]=dip
        return out
    ddips=get_dip(xx_f)

    def get_dep(xf):
        global XF, XG, DIP, DEP
        out=zeros_like(xf)
        x=asarray(xf,dtype='float')
        _x=zeros_like(x)

        ch=(xf<XF[0])
        out[ch]=DEP[0]
        ch= (xf>XF[-1])
        out[ch]=DEP[-1]

        for nth in range(1,len(XG)):
            ch= (x>=XF[nth-1])&(x<=XF[nth])
            _x[ch]=DEP[nth-1]-(x[ch]-XF[nth-1])*sin(DIP[nth-1])
        return _x

    def _mesh_grids_on_fault(self):
        

        self.num_subflt_along_strike = 11
        self.num_subflt_along_dip = 26

        # Grid point along width of fault in fault coordinates
        self.x_f = linspace(0, self.flt_wid, self.num_subflt_along_strike)
        self.subflt_dim_dip = x_f[1]-x_f[0]

        # Grid point along length of fault in fault coordinates
        self.y_f = linspace(0,flt_len, self.num_subflt_along_dip)
        self.subflt_dim_strike = y_f[1]-y_f[0]

        self.xx_f, self.yy_f = meshgrid(x_f,y_f)
