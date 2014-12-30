import os

from .gmt_guru import GMTGuru
from .gmt_plot import GMTPlot
from .utils import _assert_file_name_extension

class GMT(GMTGuru):
    def __init__(self):
        super().__init__()
        self.gplt = GMTPlot()

    def save_stdout(self, filename):
        with open(filename, 'wb') as fid:
            fid.write(self.stdout)

    def save_stderr(self, filename):
        with open(filename, 'wb') as fid:
            fid.write(self.stderr)

    def save(self, filename):
        fn, ext = os.path.splitext(filename)
        if ext == '.ps':
            self.save_ps(filename)
        elif ext == '.pdf':
            self.save_pdf(filename)
        else:
            raise NotImplementedError()

        self._clean()
        

    def save_ps(self, filename):
        self.gplt.save_ps(filename)

    def save_pdf(self, filename, **kwargs):
        _assert_file_name_extension(filename, '.pdf')
        fn, ext = os.path.splitext(filename)
        self.save_ps(fn + '.ps')        
        self.ps2raster(fn + '.ps', T='f', **kwargs)
        os.remove(fn + '.ps')

    def save_shell_script(self, filename, output_file=None):
        self.gplt.save_shell_script(filename, output_file)

    def _clean(self):
        trash_files = ['gmt.conf', 'gmt.history']
        for file in trash_files:
            if os.path.exists(file):
                os.remove(file)



    
        
        
