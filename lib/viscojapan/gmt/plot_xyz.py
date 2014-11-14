from os.path import exists, join
from os import makedirs
import tempfile

import pGMT

from .utils import topo_cpts

__all__ = ['GMTXYZ']

class GMTXYZ(object):
    def __init__(self,
                 gplt,
                 file_xyz,
                 if_log_color_scale = True,
                 cpt_scale = '-4/0.6/0.01',
                 workdir = '~tmp',
                 ):
        self.gplt = gplt
        self.file_xyz = file_xyz
        self.if_log_color_scale = if_log_color_scale
        self.cpt_scale = cpt_scale

        self._workdir = workdir
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
        gmt = pGMT.GMT()
        gmt.nearneighbor(
            self.file_xyz,
            G = self.xyz_grd,
            I='1k', N='8', R='', S='60k'
            )

    def _prepare_cpt_file(self):
        self.cpt_file = join(self._workdir, 'cpt')
        gmt = pGMT.GMT()
        kwargs = {'C' : topo_cpts['seminf-haxby'],
                  'T' : self.cpt_scale,
                  'M' : ''}
        if self.if_log_color_scale:
            kwargs['Q']=''
        
        gmt.makecpt(**kwargs)
            
        gmt.save_stdout(self.cpt_file)

    def plot_xyz(self):
        self.gplt.grdimage(
            self.xyz_grd,
            J='', R='', C=self.cpt_file,
            O='',K='', Q='',
            )
        
        # fill water with white color
        self.gplt.pscoast(R='', J='', S='white', O='', K='')

    def plot_scale(self, scale_interval='a'):
        if self.if_log_color_scale:
            Q = ''
        else:
            Q = None
            
        self.gplt.psscale(
            D='4/9/4/.2',
            B='%s::/:m:'%scale_interval, O='', K='',
            C=self.cpt_file,Q=Q)

    def plot_contour(self,
                     contours = [5, 10 , 20, 40, 60],
                     W = 'thickest',):
        _txt = ''
        for ii in contours:
            _txt += '%f A\n'%ii
            
        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write(_txt)
            fid.seek(0,0)
            self.gplt.grdcontour(
                self.xyz_grd,
                C=fid.name,
                A='1+f9+um',
                G='n1/.5c', J='', R='', O='',K='',
                W = W,
                )
        


    
