from numpy import ascontiguousarray, asarray
from pylab import plt

import viscojapan as vj

from .map_plot import MapPlot
from ..fault_model import FaultFileIO
from ..utils import assert_file_exists
from ..epochal_data import EpochalSlip, EpochalIncrSlip

class MapPlotFault(MapPlot):
    def __init__(self, fault_file, basemap = None):
        super().__init__(basemap = basemap)
        self.fault_file = fault_file

        self._init_fault_file()

    def _init_fault_file(self):
        assert_file_exists(self.fault_file)
        self.fault_file_obj =  FaultFileIO(self.fault_file)

    def _reshape_as_fault(self, arr):        
        ny = self.fault_file_obj.num_subflt_along_dip
        nx = self.fault_file_obj.num_subflt_along_strike
        return arr.reshape([ny,nx])

    def pcolor_on_fault(self, val, **kwargs):
        LLons = self.fault_file_obj.LLons
        LLats = self.fault_file_obj.LLats

        vval = self._reshape_as_fault(val)
        
        return self.basemap.pcolor(LLons, LLats, vval, latlon=True,
                            **kwargs)
        
    def plot_slip(self, m, cmap=None, clim=None):        
        self.pcolor_on_fault(m, cmap = cmap) 
        cb = plt.colorbar()
        plt.clim(clim)
        cb.set_label('slip(m)')

    def contour_on_fault(self, val, **kwargs):
        LLons = self.fault_file_obj.LLons[1:,1:]
        LLats = self.fault_file_obj.LLats[1:,1:]
        
        vval = self._reshape_as_fault(val)
        
        CS = self.basemap.contour(LLons, LLats, vval,
                             latlon=True, **kwargs)
        return CS
        
    def plot_slip_contours(self, m, colors='white', V=None):
        CS = self.contour_on_fault(m, colors=colors, V=V)
        plt.clabel(CS, inline=1, fontsize=10)

    def plot_slip_file_contours(self, f_slip, epoch):
        slip_obj = EpochalSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip_contours(slip)

    def plot_incr_slip_file_contours(self, f_slip, epoch):
        slip_obj = EpochalIncrSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip_contours(slip)   
        

    def plot_fault(self,fno=None,ms=15, color='gray'):
        
        LLons = self.fault_file_obj.LLons
        LLats = self.fault_file_obj.LLats
        
        assert ms<250 and ms>=0, "Fault No. out of range."
            
        self.basemap.plot(LLons,LLats,color=color, latlon=True)
        self.basemap.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color=color, latlon=True)
        if fno is not None:
            xpt,ypt=self.basemap(LLons,LLats)
            xpt1=xpt[0:-1,0:-1]
            ypt1=ypt[0:-1,0:-1]

            xpt2=xpt[1:,1:]
            ypt2=ypt[1:,1:]

            x0=(xpt1.flatten()[fno]+xpt2.flatten()[fno])/2.
            y0=(ypt1.flatten()[fno]+ypt2.flatten()[fno])/2.
            
            self.basemap.plot(x0,y0,marker='*',color='red',ms=ms)


    def plot_incr_slip_file(self, f_slip, epoch):
        slip_obj = EpochalIncrSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip(slip)

    def plot_slip_file(self, f_slip, epoch):
        slip_obj = EpochalSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip(slip)
