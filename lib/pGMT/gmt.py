from .gmt_guru import GMTGuru
from .gmt_plot import GMTPlot

class GMT(GMTGuru):
    def __init__(self):
        super().__init__()
        self.gplt = GMTPlot()


    
        
        
