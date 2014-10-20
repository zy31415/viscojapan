from .my_basemap import MyBasemap

import viscojapan as vj

__all__ = ['plot_epicenter']

def plot_epicenter(basemap=None , marker='*' , ms=15, color='red',
                   **kwargs):
    if basemap is None:
        basemap = MyBasemap()
           
    x0 = vj.TOHOKU_EPICENTER[0]
    y0 = vj.TOHOKU_EPICENTER[1]

    basemap.plot(x0,y0, latlon=True, marker=marker ,color=color, ms=ms, **kwargs)
