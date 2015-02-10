

__all__ = ['Site']

class Site(object):
    ''' Represent a site.
    Keep this class simple.
    Remember Single Responsibility Principle
'''
    def __init__(self,
                 id = None,
                 lon = None,
                 lat = None
                 ):
        self._id = id
        self._lon = lon
        self._lat = lat

    @property
    def id(self) -> str:
        return self._id

    @property
    def lon(self) -> bool:
        return self._lon        

    @property
    def lat(self) -> bool:
        return self._lat

    @property
    def if_seafloor(self)  -> bool:
        if self._id[0] == '_':
            return True
        else:
            return False

    @property
    def if_onshore(self) -> bool:
        if self._id[0] == '_':
            return False
        else:
            return True

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        out = '{id} ({lon:.5f},{lat:.5f})'.format(
            id=self.id, lon=self.lon, lat=self.lat)
        return out

