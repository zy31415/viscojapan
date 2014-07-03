from numpy import ascontiguousarray, asarray
from pylab import plt

from .map_plot import MapPlot
from ..fault_model import FaultFileIO
from ..utils import _assert_file_exists, kw_init
from ..epochal_data import EpochalSlip, EpochalIncrSlip

class MapPlotFault(MapPlot):
    def __init__(self, fault_file, **kwargs):
        super().__init__()
        self.fault_file = fault_file
        kw_init(self, kwargs)

        self._init_fault_file()

    def _init_fault_file(self):
        _assert_file_exists(self.fault_file)
        self.fault_file_obj =  FaultFileIO(self.fault_file)

    def _assert_slip_array_shape(self, slip):
        sh = slip.shape
        assert len(sh) == 2 , 'Input slip should be column vector or matrix.'
        
        ny = self.fault_file_obj.num_subflt_along_dip
        nx = self.fault_file_obj.num_subflt_along_strike

        if sh[1]==1:
            assert sh[0] == nx*ny, 'Misshape!'
        else:
            assert sh[0] == ny, 'Misshape!'
            assert sh[1] == nx, 'Misshape!'

        return slip.reshape([ny,nx])
        
    def plot_slip(self, m, cmap=None, clim=None):
        '''
'''
        m = asarray(m)
        LLons = self.fault_file_obj.LLons
        LLats = self.fault_file_obj.LLats

        mm = self._assert_slip_array_shape(m)

        self.basemap.pcolor(LLons,LLats,mm,latlon=True,cmap=cmap)        
        cb = plt.colorbar()
        plt.clim(clim)
        cb.set_label('slip(m)')

##        com_mo = ComputeMoment()
##        com_mo.fault_file = self.fault_file
##        
##        mo, mw = com_mo.moment(m)
##        
##        title('Mo=%.3g,Mw=%.2f'%(mo,mw))

    def plot_slip_contours(self, m, colors='white', V=None):
        LLons = self.fault_file_obj.LLons[1:,1:]
        LLats = self.fault_file_obj.LLats[1:,1:]
            
        mm = self._assert_slip_array_shape(m)
        
        CS = self.basemap.contour(LLons,LLats,mm,latlon=True, colors=colors, V=V)
        plt.clabel(CS, inline=1, fontsize=10)

    def plot_slip_file_contours(self, f_slip, epoch):
        slip_obj = EpochalSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip_contours(slip)

    def plot_incr_slip_file_contours(self, f_slip, epoch):
        slip_obj = EpochalIncrSlip(f_slip)
        slip = slip_obj(epoch)
        self.plot_slip_contours(slip)   
        

    def plot_fault(self,fno=None,ms=15):
        
        LLons = self.fault_file_obj.LLons
        LLats = self.fault_file_obj.LLats
        
        assert ms<250 and ms>=0, "Fault No. out of range."
            
        self.basemap.plot(LLons,LLats,color='gray',latlon=True)
        self.basemap.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color='gray',latlon=True)
        if fno is not None:
            xpt,ypt=self(LLons,LLats)
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
