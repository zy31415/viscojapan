import tempfile

import numpy as np

import pGMT
from ....inversion import ResultFileReader
from ....fault_model import FaultFileReader
from ....moment import ComputeMoment
from ....utils import get_middle_point

from .plot_slip import _PlotSlip
from ..plotter import Plotter

__all__ = ['PlotSlipResult']


class PlotSlipResult(Plotter):
    def __init__(self,                 
                 fault_file,
                 result_file,
                 subplot_width = 3.2,
                 subplot_height = 5.2,
                 num_plots_per_row = 5,
                 color_label_interval_co = 20,
                 color_label_interval_aslip = 3,
                 earth_file = None
                 ):
        super().__init__()
        self.fault_file = fault_file
        self.result_file = result_file

        self.subplot_width = subplot_width
        self.subplot_height = subplot_height

        self.num_plots_per_row = num_plots_per_row
        self.color_label_interval_co = color_label_interval_co
        self.color_label_interval_aslip = color_label_interval_aslip

        self.earth_file = earth_file

    def plot(self, out_file):
        super().plot(out_file)
        self._get_info_from_fault_file_and_result_file()

        self.gmt = gmt = pGMT.GMT()
        self.gplt = gplt = gmt.gplt        

        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','6',
                   'LABEL_FONT_SIZE','6',
                   'FONT_ANNOT_PRIMARY','4',
                   'MAP_FRAME_TYPE','plain',
                   'MAP_FRAME_PEN','thinner,black',
                   'PS_MEDIA','letter',
                   'MAP_TICK_LENGTH_PRIMARY','.05',
                   'MAP_ANNOT_OFFSET_PRIMARY','.05')

        self._plot_coseismic_slip()

        # plot afterslip:
        self._num_of_subplots_in_a_row = 1
        for nth, si in enumerate(self.slip[1:,:,:],1):
            offset_X, offset_Y = self._next_offset()

            _plt = self._plot_afterslip_at_nth_epoch(
                nth = nth,
                offset_X = offset_X,
                offset_Y = offset_Y
                )
            if nth ==1:
                _plt.add_psscale(
                    gridline_interval = self.color_label_interval_aslip)                


        gplt.finish()
            
        gmt.save(out_file)

    def _get_info_from_fault_file_and_result_file(self):        
        freader = FaultFileReader(self.fault_file)
        fault_shape = (freader.num_subflt_along_dip,
                       freader.num_subflt_along_strike)
        num_slip_pars = freader.num_subflt_along_dip * freader.num_subflt_along_strike

        llons = freader.LLons
        llats = freader.LLats
        self.lats = get_middle_point(llats)
        self.lons = get_middle_point(llons)

        reader = ResultFileReader(self.result_file)
        self.epochs = reader.epochs
        self.num_epochs = reader.num_epochs
        self.slip = reader.incr_slip.reshape(
            (self.num_epochs,freader.num_subflt_along_dip, freader.num_subflt_along_strike))
        self.max_aslip = np.amax(self.slip[1:,:,:])
        self.co_slip = self.slip[0,:,:]
        self.max_co_slip = np.amax(self.co_slip)        


    def _plot_coseismic_slip(self):
        _plt = _PlotSlip(
            self.gmt,
            self.lons,
            self.lats,
            self.co_slip,
            cpt_max_slip = self.max_co_slip,
            offset_Y = 22,
            offset_X = 1.5,
            size = '3c',
            if_boundary_annotation = True,
            if_map_scale = True,
            if_slab_annotation = True
            )
        _plt.plot(K='')
        Mo, Mw = self.compute_Mo_Mw(self.co_slip)
        _plt.add_psscale(gridline_interval='20')
        _plt.add_annotation(
            day = '0 (mainshock)',
            Mo = '%.4G'%Mo,
            Mw = '%.2f'%Mw,
            K = '')

    def _plot_afterslip_at_nth_epoch(self, nth, offset_X, offset_Y):
        slip = self.slip[nth,:,:]
        plt = _PlotSlip(
            self.gmt,
            self.lons,
            self.lats,
            slip = slip,
            cpt_max_slip = self.max_aslip,
            offset_X = offset_X,
            offset_Y = offset_Y,
            size = '3c',
            O = ''
            )
        plt.plot(K='')
        Mo, Mw = self.compute_Mo_Mw(slip)
        plt.add_annotation(
            day = '%d ~ %d'%(self.epochs[nth-1], self.epochs[nth]),
            Mo = '%.4G'%Mo,
            Mw = '%.2f'%Mw,
            K = '')
        return plt

    def _next_offset(self):
        offset_X = self.subplot_width
        offset_Y = 0
        if self._num_of_subplots_in_a_row > (self.num_plots_per_row - 1):
            offset_Y = -self.subplot_height
            offset_X *= - (self.num_plots_per_row-1)
            self._num_of_subplots_in_a_row = 0

        self._num_of_subplots_in_a_row += 1
            
        return offset_X, offset_Y
        

    def compute_Mo_Mw(self, slip):
        com = ComputeMoment(self.fault_file, self.earth_file)
        return com.compute_moment(slip)
    
