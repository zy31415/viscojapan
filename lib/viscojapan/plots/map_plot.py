from .my_basemap import MyBasemap

class MapPlot(object):
    def __init__(self, basemap = None):
        if basemap is None:
           basemap = MyBasemap() 
        self.basemap = basemap
        
