##from os.path import exists,join,basename, dirname
##from os import makedirs
##from tsana.date_utils import *
##from subprocess import Popen, check_output
##import sys
##from tempfile import TemporaryFile, mkdtemp
##from time import time
##from shutil import copyfile, rmtree

from .pollitz_wrapper import PollitzWrapper

class StrainA(PollitzWrapper):
    ''' Class wraper of VISCO1D command strainA
'''
    def __init__(self,
                 earth_dir,
                 file_flt,
                 file_sites,
                 file_out,
                 days_after,
                 if_skip_on_existing_output = True
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

        self.days_after = self.days_after
        
        self.earth_files=['earth.model',
                         'decay.out','decay4.out',
                         'vsph.out','vtor.out']

        self._cmd = 'strainA'

    @overrides(PollitzWrapper)
    def gen_stdin(self):
        ''' Form the stdin for command strainA.
'''
        t1=asdyr(self.t_eq)
        t2=asdyr(self.t_eq+self.days_after)
        # temporary file:
        stdin=TemporaryFile('r+')
        stdin.write('Comment Line.\n')
        stdin.write(check_output("grep -v '#' %s | head -n 1"\
                                 %(self.file_flt),shell=True).decode())
        stdin.write("%f %f %f 1.\n"%(t1,t1,t2))
        stdin.write(check_output("grep -v '#' %s | tail -n +2"\
                                 %(self.file_flt),shell=True).decode())
        stdin.write(check_output("grep -v '#' %s | wc -l"\
                                 %(self.file_sites),shell=True).decode())
        stdin.write(check_output("grep -v '#' %s"\
                                 %(self.file_sites),shell=True).decode())
        stdin.write("0\n")
        stdin.write("0\n")
        stdin.write("out")
        stdin.seek(0)
        return stdin
