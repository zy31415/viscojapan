import tempfile

import numpy as np

import pGMT
from ...inversion import ResultFileReader
from ...fault_model import FaultFileReader
from ...utils import get_middle_point

from .plot_slip import PlotSlip

__all__ = ['PlotSlipResult']

def makecpt(gmt, max_slip, incr, out_cpt):
    gmt.makecpt(
    C='hot',
    T='0/%f/%f'%(max_slip, incr),
    I='')
    gmt.save_stdout(out_cpt)

class PlotSlipResult(object):
    def __init__(self,                 
                 fault_file,
                 result_file,
                 out_file,
                 subplot_width = 3.2,
                 subplot_height = 5.2,
                 num_plots_per_row = 5,
                 color_label_interval_co = 20,
                 color_label_interval_aslip = 3,
                 ):
        self.fault_file = fault_file
        self.result_file = result_file
        self.subplot_width = subplot_width,
        self.subplot_height = subplot_height,
        self.num_plots_per_row = num_plots_per_row,
        self.color_label_interval_co = color_label_interval_co,
        self.color_label_interval_aslip = color_label_interval_aslip,

    def plot(out_file):
        freader = FaultFileReader(fault_file)
        fault_shape = (freader.num_subflt_along_dip,
                       freader.num_subflt_along_strike)
        num_slip_pars = freader.num_subflt_along_dip * freader.num_subflt_along_strike

        llons = freader.LLons
        llats = freader.LLats
        lats = get_middle_point(llats)
        lons = get_middle_point(llons)

        reader = ResultFileReader(result_file)
        num_epochs = reader.num_epochs
        slip = reader.incr_slip.reshape(
            (-1,freader.num_subflt_along_dip, freader.num_subflt_along_strike))
        max_aslip = np.amax(slip[1:,:,:])
        co_slip = slip[0,:,:]
        max_co_slip = np.amax(co_slip)


        ################
        gmt = pGMT.GMT()
        gplt = gmt.gplt

        cpt_co = tempfile.NamedTemporaryFile('w+t')
        makecpt(gmt, max_co_slip,5, cpt_co.name)
        cpt_co.seek(0,0)

        cpt_aslip = tempfile.NamedTemporaryFile('w+t')
        makecpt(gmt, max_aslip,1, cpt_aslip.name)
        cpt_aslip.seek(0,0)

        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','6',
                   'LABEL_FONT_SIZE','6',
                   'FONT_ANNOT_PRIMARY','4',
                   'MAP_FRAME_TYPE','plain',
                   'MAP_FRAME_PEN','thinner,black',
                   'PS_MEDIA','letter',
                   'MAP_TICK_LENGTH_PRIMARY','.05',
                   'MAP_ANNOT_OFFSET_PRIMARY','.05')

        ## plot coseismic slip:
        PlotSlip(
            gmt,
            lons,
            lats,
            slip[0,:,:],
            cpt_file = cpt_co.name,
            offset_Y = 22,
            offset_X = 1.5,
            size = '3c',
            if_boundary_annotation = True,
            if_map_scale = True,
            if_slab_annotation = True,
            if_psscale = True,
            psscale_gridline_interval = color_label_interval_co,
            ).plot()

        # plot the first afterslip:
        PlotSlip(
            gmt,
            lons,
            lats,
            slip = slip[1,:,:],
            cpt_file = cpt_aslip.name,
            offset_X = subplot_width,
            size = '3c',
            if_psscale = True,
            psscale_gridline_interval = color_label_interval_aslip,
            O = '').plot()

        ## plot afterslip:
        nth_in_a_row = 2
        for nth, si in enumerate(slip[2:,:,:],3):
            offset_X = subplot_width
            offset_Y = 0
            if nth_in_a_row > (num_plots_per_row-1):
                offset_Y = -subplot_height
                offset_X *= - (num_plots_per_row-1)
                nth_in_a_row = 0

            if nth >= num_epochs:
                K = None
            else:
                K = ''
            PlotSlip(
                gmt,
                lons,
                lats,
                slip = si,
                cpt_file = cpt_aslip.name,
                offset_X = offset_X,
                offset_Y = offset_Y,
                size = '3c',
                O = '',
                K = K
                ).plot()
            nth_in_a_row += 1
            
        gmt.save(out_file)

        cpt_co.close()
        cpt_aslip.close()



