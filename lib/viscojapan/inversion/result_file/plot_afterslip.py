import tempfile

import numpy as np

import pGMT

from ...gmt.gadgets import plot_seafloor_stations, plot_slab
from ...fault_model import FaultFileReader
from ...utils import get_middle_point

__author__ = 'zy'

__all__ = ['AfterslipPlotter']

class AfterslipPlotter(object):
    def __init__(self,
                 slip,
                 epochs,
                 fault_file,
                 cpt_file = 'hot',
                 cpt_reverse = True,
                 max_slip = None,
                 ):
        self.slip = slip

        assert len(epochs) == 9, '9 epochs!'
        self.epochs = epochs


        self.slip = self.slip.respace(epochs)

        self.fault_file = fault_file
        self.cpt_file = cpt_file
        self.cpt_reverse = cpt_reverse

        self.max_slip = max_slip


    def init(self):
        self.gmt = pGMT.GMT()
        self.gplt = self.gmt.gplt

        self.gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','10',
                   'LABEL_FONT_SIZE','6',
                   'FONT_ANNOT_PRIMARY','10',
                   'MAP_FRAME_TYPE','plain',
                   'MAP_FRAME_PEN','thinner,black',
                   'PS_MEDIA','letter',
                   'MAP_TICK_LENGTH_PRIMARY','.05',
                   'MAP_ANNOT_OFFSET_PRIMARY','.05')

        self._make_cpt_file()


    def plot(self):

        size = '3.8'
        X0 = '1'
        Y0 = '20'
        X = float(size)
        Y = -5.7815
        padding = 0.2

        self.init()

        # first row
        self._subplot_slip(nth_section=1, size=size, offset_X=X0, offset_Y=Y0, B='2WeNs', O=None)
        self._subplot_slip(nth_section=2, size=size, offset_X=X, offset_Y='0', B='2weNs', O='')
        self._subplot_slip(nth_section=3, size=size, offset_X=X, offset_Y='0', B='2weNs', O='')
        self._subplot_slip(nth_section=4, size=size, offset_X=X, offset_Y='0', B='2weNs', O='')
        self._subplot_slip(nth_section=5, size=size, offset_X=X, offset_Y='0', B='2weNs', O='')

        # second row
        self._subplot_slip(nth_section=6, size=size, offset_X='%fc'%(-4*float(X)), offset_Y=Y, B='2Wens', O='')
        self._subplot_slip(nth_section=7, size=size, offset_X=X, offset_Y='0', B='2wens', O='')
        self._subplot_slip(nth_section=8, size=size, offset_X=X, offset_Y='0', B='2wens', O='')

        # plot color scale
        self._plot_psscale()

        # plot Mo-Mw
        self._suplot_Mo_Mw(offset_X=X+X*padding, offset_Y=-Y*padding, B='2wens', O='')


    def _subplot_slip(self, nth_section,
                      size, offset_X, offset_Y, B, O=None):

        lon1 = 139.7
        lon2 = 144.7
        lat1 = 34.7
        lat2 = 40.7

        self.gplt.psbasemap(
            R = '{lon1}/{lon2}/{lat1}/{lat2}'.format(lon1=lon1,
                                     lon2=lon2,
                                     lat1 = lat1,
                                     lat2 = lat2
                                     ),
            JM = '141.5/38/%s'%size, # projection
            B = B, U='18/25/0',
            P='',K='', O=O,
            X = offset_X,
            Y = offset_Y,
        )

        self._plot_slip_on_fault(nth_section)

        self.gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,150,-.',
            W = 'faint,dimgray',A='1000',L=None,
            O = '', K='')

        plot_seafloor_stations(self.gplt, marker_size=0.1,
                               lw='faint',color='green',
                               fontsize=None
                               )

        plot_slab(self.gplt,
                  color='dimgray', lw='faint',
                  label_line = '144/41/138/41',
                  label_font_size = '4',
                  label_color = 'dimgray',
                  K = '',
                  if_contour_annotation = True,
                  )

    def _plot_slip_on_fault(self, nth_section):

        grd_file = tempfile.NamedTemporaryFile(suffix='.grd')

        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write(self._form_slip_xyz_file_string(nth_section))
            fid.seek(0,0)
            self.gmt.nearneighbor(
                fid.name,
                R='',
                I='2k',
                G = grd_file.name,
                N='8',
                S='40k')

            self.gplt.grdimage(
                grd_file.name,
                J='', R='', C=self._cpt.name,
                O='',K='', Q='',
                )
        grd_file.close()

        day1 = self.epochs[nth_section-1]
        day2 = self.epochs[nth_section]
        self._add_annotation(day1, day2)

    def _form_slip_xyz_file_string(self, nth_section):
        s = self.slip.get_incr_slip_at_nth_epoch(nth_section)

        freader = FaultFileReader(self.fault_file)

        llons = freader.LLons_mid
        llats = freader.LLats_mid

        _txt = ''
        for lon, lat, s in zip(np.nditer(llons.flatten()),
                               np.nditer(llats.flatten()),
                               np.nditer(s.flatten())):
            _txt +='%f %f %f\n'%(lon, lat, s)
        return _txt

    def _suplot_Mo_Mw(self, offset_X, offset_Y, B, O=None):

        self.gplt.psbasemap(
        R = '140/145/35/41.5',       # region
        JX = '3c/3d', # projection
        B = B, U='18/25/0',
        P='',K='', O=O,
        X = offset_X,
        Y = offset_Y,
        )

    def _make_cpt_file(self):
        if self.cpt_reverse:
            I = ''
        else:
            I = None

        if self.max_slip is None:
            max_slip = np.amax(self.slip.get_incr_slip_3d()[1:,:,:])

        cpt = tempfile.NamedTemporaryFile('w+t',suffix='.cpt')
        incr = max_slip/30.
        self.gmt.makecpt(
            C=self.cpt_file,
            T='0/%f/%f'%(max_slip, incr),
            I=I)
        self.gmt.save_stdout(cpt.name)
        cpt.seek(0,0)

        self._cpt = cpt

    def _add_annotation(self, day1, day2, font_size='8'):
        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write('''#
H {font_size} Times-Roman {day1} ~ {day2} d
'''.format(
                day1 = day1,
                day2 = day2,
                font_size = font_size,
            ))

            fid.seek(0,0)

            self.gplt.pslegend(
                fid.name,
                D='143.5/35.3/1/0.3/MC',
                R='', J='', O='', K='')

    def _plot_psscale(self, gridline_interval='.2',):
        self.gplt.psscale(
            D = '-3/-.2/6/.3h',
            B = '%s::/:m:'%gridline_interval,
            O = '', K='',
            C = self._cpt.name)

    def save(self, fn):
        self.gmt.gplt.finish()
        self.gmt.save(fn)


