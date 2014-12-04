from os.path import exists, join
from os import makedirs
import tempfile

import pGMT

from .utils import topo_cpts

__all__ = ['GMTXYZ']

class GMTXYZ(object):
    def __init__(self,
                 gmt,
                 file_xyz,
                 if_log_color_scale = True,
                 cpt_scale = '-4/0.6/0.01',
                 workdir = '~tmp',
                 interp_inc = '1k',
                 ):
        self.gmt = gmt
        self.file_xyz = file_xyz
        self.if_log_color_scale = if_log_color_scale
        self.cpt_scale = cpt_scale

        self._workdir = workdir
        self.interp_inc = interp_inc
        
        self._init()
        

    def _init(self):
        self._init_working_dir()
        self._interpolate_xyz_to_grd()
        self._prepare_cpt_file()

    def _init_working_dir(self):
        if not exists(self._workdir):
            makedirs(self._workdir)

    def _interpolate_xyz_to_grd(self):
        self.xyz_grd = join(self._workdir, 'grd')
##        self.gmt.nearneighbor(
##            self.file_xyz,
##            G = self.xyz_grd,
##            I=self.interp_inc,
##            N='8',
##            R='',
##            S=self.interp_searching_radius,
##            )
        self.xyz_grd = join(self._workdir, 'grd')
        self.gmt.xyz2grd(
            self.file_xyz,
            G = self.xyz_grd,
            I = self.interp_inc,
            R = '',
            )

    def _prepare_cpt_file(self):
        self.cpt_file = join(self._workdir, 'cpt')
        kwargs = {'C' : topo_cpts['seminf-haxby'],
                  'T' : self.cpt_scale,
                  'D' : '',
                  'M' : ''}
        if self.if_log_color_scale:
            kwargs['Q']=''
        
        self.gmt.makecpt(**kwargs)
            
        self.gmt.save_stdout(self.cpt_file)

    def plot_xyz(self):
        self.gmt.gplt.grdimage(
            self.xyz_grd,
            J='', R='', C=self.cpt_file,
            O='',K='', Q='',
            )

    def maskout_water(self, A='500k', D='h'):
        file_mask = join(self._workdir, 'land_mask.grd')
        self.gmt.grdlandmask(R='', A=A, D=D, I = self.interp_inc,
                        N='NaN/1',G=file_mask)
        self.gmt.grdmath(self.xyz_grd, file_mask, 'OR', '= ', self.xyz_grd)

    def plot_scale(self, x=4,y=9,scale_interval='a'):
        if self.if_log_color_scale:
            Q = ''
        else:
            Q = None
            
        self.gmt.gplt.psscale(
            D='%f/%f/4/.2'%(x,y),
            B='%s::/:m:'%scale_interval, O='', K='',
            C=self.cpt_file,Q=Q)

    def plot_contour(self,
                     contours = [5, 10 , 20, 40, 60],
                     W = 'thickest',
                     label_line = None,
                     label_font_size = 9,
                     smooth_factor = 8
                     ):
        _txt = ''
        for ii in contours:
            _txt += '%f A\n'%ii
            
        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write(_txt)
            fid.seek(0,0)
            if label_line is None:
                G = 'n1/.5c'
            else:
                G = label_line
            self.gmt.gplt.grdcontour(
                self.xyz_grd,
                C=fid.name,
                A='1+f%f+um'%label_font_size,
                G=G, J='', R='', O='',K='',S='4',
                W = W,
                )
        
