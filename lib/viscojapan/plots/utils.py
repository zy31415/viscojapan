import numpy as np
from pylab import plt
import matplotlib
import matplotlib.ticker as ticker


from .my_basemap import region_ranges
from ..utils import mw_to_mo, mo_to_mw

__all__=['plot_box_on_basemap','plot_regions_on_basemap','plot_Mos_Mws']

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
    
def plot_Mos_Mws(days, Mos=None, Mws=None, ylim = None, yticks=None):
    if Mos is None and Mws is None:
        raise ValueError('Set Mos or Mws.')
    if Mos is not None and Mws is not None:
        raise ValueError("Don't set both.")
    if Mws is not None:
        Mos = mw_to_mo(Mws)
        
    fig, ax1 = plt.subplots()
    ax1.plot(days, Mos,'-o')
    ax1.set_yscale('log')

    if yticks is not None:
        ax1.set_yticks(yticks)
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    if ylim is not None:
        ax1.set_ylim(ylim)

    lim1 = ax1.get_ylim()
    
    ax1.set_xlabel('days after the mainshock')
    ax1.set_ylabel('Moment(Nm)')
    ax1.grid('on')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Mw')
    ax2.set_ylim(mo_to_mw(lim1))
