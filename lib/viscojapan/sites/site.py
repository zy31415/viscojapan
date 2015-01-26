import pyproj as pj

class Site(object):
    ''' Represent a site.
'''
    def __init__(self,
                 id = None,
                 name = None,
                 lon = None,
                 lat = None
                 ):
        self._id = id
        self._name = name        
        self._lon = lon
        self._lat = lat

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def lon(self) -> bool:
        return self._lon        

    @property
    def lat(self) -> bool:
        return self._lat

    @property
    def if_seafloor(self)  -> bool:
        if self._name[0] == '_':
            return True
        else:
            return False

    @property
    def if_onshore(self) -> bool:
        if self._name[0] == '_':
            return False
        else:
            return True

    @property
    def epi_dist(self) -> float:
        ''' Distance from the epicenter in KM.
'''
        epi_lon0, epi_lat0 = vj.TOHOKU_EPICENTER
        p = pj.Geod(ellps='WGS84')
        az1, az2, dis = p.inv(self.lon, self.lat, epi_lon0, epi_lat0)
        return dis/1000.

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        out = '%s at (%8.4f, %8.4f), %8.3f km from the epi.'%\
               (self.name, self.lon, self.lat, self.epi_dist)
        #out += '\n  %s\n'%(super().__str__())
        return out
        
