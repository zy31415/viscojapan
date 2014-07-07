##from os.path import exists,join,basename, dirname
##from os import makedirs
##from subprocess import Popen, check_output
##import sys
from tempfile import TemporaryFile
##from time import time
##from shutil import copyfile, rmtree

from .pollitz_wrapper import PollitzWrapper
from ..utils import overrides

class Stat2gA(PollitzWrapper):
    ''' Class wraper of VISCO1D command strainA
'''
    def __init__(self,
                 earth_dir,
                 file_flt,
                 file_sites,
                 file_out,
                 if_skip_on_existing_output = True
                 stdout = sys.stdout,
                 stderr = sys.stderr,
                 ):
        super().__init__(
            earth_dir = file_flt,
            file_flt = file_flt,
            file_sites = file_sites,
            file_out = file_out,
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )

        self.earth_files=['earth.model_stat','stat0.out']

        self._cmd = 'stat2gA'

    @overrides(PollitzWrapper)
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



    
