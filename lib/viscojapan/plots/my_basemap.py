from numpy import arange
from mpl_toolkits.basemap import Basemap
from ..utils import kw_init

class MyBasemap(Basemap):
    def __init__(self, **kwargs):
        # initialization parameters and default value
        self.region_box = None
        self.region_code = 'near'
        self.x_interval=2.
        self.y_interval=2.

        kw_init(self, kwargs)
        
        self._init()

    def _init_set_region_box_by_region_code(self):
        if self.region_box is None:
            if self.region_code=='I':
                self.region_box=(128,30,132.5,34.5)
            elif self.region_code=='A':
                self.region_box=(136.2,35.8,142.6,38.2)
            elif self.region_code=='H':
                self.region_box=(131,33,137,36.5)
                self.region_box=(140,41.8,146.2,45.8)
            elif self.region_code=='near':
                self.region_box=(136,34,146,42)
            elif self.region_code=='all':
                self.region_box=(136,34,146,42)
            else:
                raise ValueError('Invalid Region code.')
        
    def _init_draw_background(self):
        self.drawcoastlines(color='green',zorder=-1)
        # draw parallels and meridians.
        self.drawparallels(arange(-80.,81.,self.y_interval),zorder=-1,labels=[1,1,0,0])
        self.drawmeridians(arange(-180.,181.,self.x_interval),zorder=-1,labels=[0,0,0,1])
        self.drawmapboundary(color='k')

    def _init_basemap(self):
        lon_0=(self.region_box[0]+self.region_box[2])/2.
        lat_0=(self.region_box[1]+self.region_box[3])/2.
        
        super().__init__(llcrnrlon=self.region_box[0],llcrnrlat=self.region_box[1],
                         urcrnrlon=self.region_box[2],urcrnrlat=self.region_box[3],
                         resolution='l',area_thresh=100.,projection='eqdc',
                         lon_0=lon_0,lat_0=lat_0,
                         lat_1=lat_0-5,lat_2=lat_0+5,
                         celestial=False)

    def _init(self):
        self._init_set_region_box_by_region_code()               
        self._init_basemap()
        self._init_draw_background()



