from tempfile import TemporaryFile

from .pollitz_wrapper import PollitzWrapper
from .utils import read_flt_file_for_stdin, read_sites_file_for_stdin

class stat2gA(PollitzWrapper):
    ''' Class wraper of VISCO1D command strainA
'''
    def __init__(self,
                 earth_model_stat = None,
                 stat0_out = None,
                 file_flt = None,
                 file_sites = None,
                 file_out = None,
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 cwd = None,
                 if_keep_cwd = False
                 ):
        self.file_flt = file_flt
        self.file_sites = file_sites
        self.file_out = file_out

        super().__init__(
            input_files = {'earth.model_stat':earth_model_stat,
                           'stat0.out':stat0_out},
            output_files = {'out':file_out},
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            cwd = cwd,
            if_keep_cwd = if_keep_cwd
            )

        self._cmd = 'stat2gA'

    def gen_stdin(self):
        ''' Form the stdin for command strainA.
'''
        # temporary file:
        stdin = TemporaryFile('r+')
        stdin.write(read_flt_file_for_stdin(self.file_flt, 'whole'))
        stdin.write(read_sites_file_for_stdin(self.file_sites))
        stdin.write("out")
        stdin.seek(0)
        return stdin



    
