import tempfile
from os.path import exists
from os import makedirs

__all__ = ['SlipPlotter']

class SlipPlotter(object):
    def __init__(self, gplt, file_slip):
        self.gplt = gplt
        self.file_slip = file_slip

        # I option, grid spacing
        self.I = '5k'
        self.low_cut_value = 1

        self._init_working_files()

    def _init_working_files(self):
        
        self._workdir = '~tmp'
        if not exists:
            makedirs(self._workdir)
        
        self._slip_grd = join(self._workdir, 'slip.grd')
        self._low_cut_grd = join(self._workdir, '~low_cut.grd')
        self._low_trench_cut_grd = join(self._workdir, '~low_trench_cut.grd')
        self._low_trench_land_cut_grd = join(self._workdir,
                                             '~low_trench_land_cut.grd')
        self._slip_cut_grd = join(self._workdir, 'slip_cut.grd')

    def _prepare_slip_file(self):
        self._interpolate_slip_file(join(self._workdir, 'slip.grd'))
        self._low_cut_slip_grd(join(self._workdir, 'slip.grd'),
                               join(self._workdir, '~slip_low_cut.grd'))
        self._trench_cut_slip_grd(join(self._workdir, '~slip_low_cut.grd'),
                               join(self._workdir, '~slip_low_trench_cut.grd'))
        self._land_cut_slip_grd(join(self._workdir, '~slip_low_trench_cut.grd'),
                               join(self._workdir, '~slip_low_trench_land_cut.grd'))

    def _interpolate_slip_file(self, out_grd):
        gmt = pGMT.GMT()
        # interpolation:
        gmt.nearneighbor(
            self.file_slip,
            G = out_grd, I=I, N='8', R='', S='100k'
            )
        
    def _low_cut_slip_grd(self, grd_in, grd_out):
        gmt = pGMT.GMT()
        gmt.grdclip(
            grd_in,
            G = grd_out,
            Sb='%f/NaN'%self.low_cut_value)
        

    def _trench_cut_slip_grd(self, grd_in, grd_out):
        gmt = pGMT.GMT()
        file_mask = join(self._workdir, 'trench_cut_mask.grd')
        gmt.grdmask(
            vj.gmt.file_kur_top,
            G = file_mask,
            A='',
            N='1/1/NaN',
            I=I,R=''
            )

        gmt.grdmath(grd_in, file_mask, 'OR', '= ', grd_out)
        
    def _land_cut_slip_grd(self, grd_in, grd_out):
        file_mask = join(self._workdir, 'land_mask.grd')
        gmt.grdlandmask(R='', Dh='', I=I,
                        N='1/NaN',G=file_mask)
        gmt.grdmath(grd_in, file_mask, 'OR', '= ', grd_out)
        
    def plot_slip():
        pass
    
        

