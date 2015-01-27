import numpy as np
from pylab import plt
import matplotlib
import matplotlib.ticker as ticker


from .my_basemap import region_ranges

__all__=['plot_box_on_basemap','plot_regions_on_basemap']

def plot_box_on_basemap(region_range,bm, ls='-', color='red'):
    lon1 = region_range[0]
    lat1 = region_range[1]
    lon2 = region_range[2]
    lat2 = region_range[3]

    lons = np.linspace(lon1, lon2, 200)
    lats = np.linspace(lat1, lat2, 200)

    bm.plot(lons, [lat1]*len(lons), ls=ls,color=color, latlon=True)
    bm.plot(lons, [lat2]*len(lons), ls=ls,color=color, latlon=True)
    bm.plot([lon1]*len(lats), lats, ls=ls,color=color, latlon=True)
    bm.plot([lon2]*len(lats), lats, ls=ls,color=color, latlon=True)

def plot_regions_on_basemap(bm):
    for code, rge in region_ranges.items():
        plot_box_on_basemap(rge, bm)

