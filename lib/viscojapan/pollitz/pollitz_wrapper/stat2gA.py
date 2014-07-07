from tempfile import TemporaryFile
from subprocess import check_output

from .pollitz_wrapper import PollitzWrapper

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
            )

        self._cmd = 'stat2gA'

    def gen_stdin(self):
        ''' Form the stdin for command strainA.
'''
        # temporary file:
        stdin = TemporaryFile('r+')
        stdin.write(check_output("grep -v '#' %s"\
                                 %(self.file_flt),shell=True).decode())
        stdin.write(check_output("grep -v '#' %s | wc -l"\
                                 %(self.file_sites),shell=True).decode())
        stdin.write(check_output("grep -v '#' %s"\
                                 %(self.file_sites),shell=True).decode())
        stdin.write("out")
        stdin.seek(0)
        return stdin



    
