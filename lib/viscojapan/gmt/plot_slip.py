import tempfile

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
        self._slip_low_cut_grd = join(self._workdir, 'slip_low_cut.grd')

    def _prepare_slip_file(self):
        gmt = pGMT.GMT()
        # interpolation:
        gmt.nearneighbor(
            self.file_slip
            G=self._slip_grd, I=I, N='8', R='', S='100k'
            )
        
    def _low_cut_slip_grd(self):
        # low cut
        gmt.grdclip(
            self._slip_grd,
            G=self._slip_low_cut_grd,
            Sb='%f/NaN'%self.low_cut_value)
        

    def _trench_cut_slip_grd(self):
        # trench cut
        gmt.grdmask(
            vj.gmt.file_kur_top,
            G='~plate_boundary_mask_file.grd',A='',
            N='1/1/NaN',
            I=I,R=''
            )

        gmt.grdmath(
            '~coseismic_slip_low_cut.grd',
            '~plate_boundary_mask_file.grd',
            'OR',
            '= ~mag.grd')
        
    def plot_slip():
        
        

