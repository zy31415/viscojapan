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
                 if_log_color_scale=True,
                 workdir = '~tmp',
                 ):
        self.gplt = gplt
        self.file_xyz = file_xyz
        self.if_log_color_scale = if_log_color_scale

        self._workdir = workdir
        

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
        if self.if_log_color_scale:
            gmt.makecpt(
                C=topo_cpts['seminf-haxby'],
                T='-4/0.6/0.01',Q='',M='')
        else:
            gmt.makecpt(
                C=topo_cpts['seminf-haxby'],
                T='-3/.6/0.1',M='')
            
        gmt.save_stdout(self.cpt_file)

    def plot_xyz(self):
        self._init()
        self.gplt.grdimage(
            self.xyz_grd,
            J='', R='', C=self.cpt_file,
            O='',K='', Q='',
            )
        
        # fill water with white color
        self.gplt.pscoast(R='', J='', S='white', O='', K='')

    def plot_scale(self):
        if self.if_log_color_scale:
            Q = ''
        else:
            Q = None
            
        self.gplt.psscale(
            D='4/9/4/.2',
            Baf='::/:m:', O='', K='',
            C=self.cpt_file,Q=Q)


    
