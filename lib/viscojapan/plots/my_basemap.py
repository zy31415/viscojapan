from numpy import arange
try:
    from mpl_toolkits.basemap import Basemap
except:
    pass
from ..utils import kw_init

__all__=['region_ranges','MyBasemap']

region_ranges = {
    'I' : (128.3,30,133,35),
    'C' : (138.8,37.9,144,40.1),
    'A' : (136.2,35.8,142.6,38.2),
    'H' : (131,33,137,36.5),
    'E' : (139,41.8,146.2,45.8),
    'near' : (136,34,146,42),
    'all' : (100,0,180,60),
    'seafloor' : (140,36,145,41),
    'ryukyu' : (120.5,23.5,131.5,32),
    'oceanward' : (135, 10, 160, 30)
    }

xy_intervals = {
    'all' : 10,
    'C' : 1,
    'oceanward' : 5,
    }

class MyBasemap(Basemap):
    def __init__(self,
                 region_box = None,
                 region_code = 'near',
                 x_interval = 2,
                 y_interval = 2.,
                 ):
        # initialization parameters and default value
        self._init_ranges_and_intervals(region_box, region_code, x_interval, y_interval)
        
        self._init()

    def _init_ranges_and_intervals(self, region_box, region_code, x_interval, y_interval):
        self.x_interval = x_interval
        self.y_interval = y_interval 
        if region_box is None:
            self.region_box = region_ranges[region_code]
            self.region_code = region_code
            if region_code in xy_intervals:
                self.x_interval = self.y_interval = xy_intervals[region_code]
        else:
            self.region_box = region_box
            self.region_code = None
            
        
    def _init_draw_background(self):
        self.drawcoastlines(color='green',zorder=-1)
        self.drawcountries(color='green', linestyle='--')
        # draw parallels and meridians.
        self.drawparallels(arange(-80.,81.,self.y_interval),zorder=-1,labels=[1,1,0,0])
        self.drawmeridians(arange(-180.,181.,self.x_interval),zorder=-1,labels=[0,0,0,1])
        self.drawmapboundary(color='k')

    def _init_basemap(self):
        lon_0=(self.region_box[0]+self.region_box[2])/2.
        lat_0=(self.region_box[1]+self.region_box[3])/2.
        
        super().__init__(llcrnrlon=self.region_box[0],llcrnrlat=self.region_box[1],
                         urcrnrlon=self.region_box[2],urcrnrlat=self.region_box[3],
                         resolution='l',area_thresh=1000.,projection='eqdc',
                         lon_0=lon_0,lat_0=lat_0,
                         lat_1=lat_0-5,lat_2=lat_0+5,
                         celestial=False)

    def _init(self):             
        self._init_basemap()
        self._init_draw_background()



