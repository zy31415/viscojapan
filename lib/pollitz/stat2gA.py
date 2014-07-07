''' Define a basic class wrapping command strainA.
The class is a subclass of Popen so it acquires all the features
that can be used to control the excution of the command.
'''
from os.path import exists,join,basename, dirname
from os import makedirs
from subprocess import Popen, check_output
import sys
from tempfile import TemporaryFile, mkdtemp
from time import time
from shutil import copyfile, rmtree

class Stat2gA(object):
    ''' Class wraper of VISCO1D command strainA
'''
    def __init__(self,
                 earth_dir,
                 file_flt,
                 file_sites,
                 file_out,
                 if_skip_on_existing_output = True
                 ):
        # The following files should be in cwd directory:
        self.earth_dir = earth_dir
        # required working files and derectories by this command:
        self.earth_files=['earth.model_stat','stat0.out']
        self.file_out = file_out

        # user inputs:
        # these files are in current work directory.
        self.file_flt = file_flt # faults file
        self.file_sites = file_sites # sites file

        self.if_skip_on_existing_output = if_skip_on_existing_output
        
        self.stdout = sys.stdout
        self.stderr = sys.stderr     

        # Change cwd for the command. See Popen page.
        # _cwd is a temporary directory.
        self._cwd = None
        self._tmp_dir = '/home/zy/tmp/'

    def _check_user_input_files(self):
        ''' Check if user input files exist:
- file_flt - fault file
- file_sites - station file
'''
        for f in [self.file_flt,self.file_sites]:
            assert exists(f), "User input file %s doesn't not exist!"%f

    def _check_earth_files(self):
        for f in self.earth_files:
            assert exists(join(self.earth_dir,f)), \
                   "Earth file %s doesn't not exist!"%f

    def _deploy(self):
        ''' Copy earth files to temporary working directory.
'''
        if not exists(self._tmp_dir):
            makedirs(self._tmp_dir)
        self._check_earth_files()
        self._cwd=mkdtemp(dir=self._tmp_dir)
        for f in self.earth_files:
            tp=join(self.earth_dir,f)
            copyfile(tp,join(self._cwd,f))

    def _form_stdin(self):
        ''' Form the stdin for command strainA.
'''
        self._check_user_input_files()
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

    def _run_commnad_in_tmp_dir(self, nice=False):
        fin=self._form_stdin()
        if nice:
            Popen(['nice','stat2gA'],
                  stdout=self.stdout,stderr=self.stderr,stdin=fin,
                  cwd=self._cwd).wait()
        else:
            Popen(['stat2gA'],
                  stdout=self.stdout,stderr=self.stderr,stdin=fin,
                  cwd=self._cwd).wait()
        fin.close()

    def _fetch_output_from_tmp_dir(self):
        dname=dirname(self.file_out)
        if dname!='':
            if not exists(dname):
                makedirs(dname)

        # fetch output from the temp dir.
        copyfile(join(self._cwd,'out'),self.file_out)   
        
    def start(self,nice=False):
        ''' Start to run the program.
'''
        if if_skip_on_existing_output and self.if_output_exist():
            return
        
        self._deploy()
        self._run_command_in_tmp_dir(nice=nice)
        self._fetch_output_from_tmp_dir()           

        # delete tmp fir
        rmtree(self._cwd)

    def if_output_exist(self):
        '''If output file exists.
'''
        if exists(self.file_out):
            return True
        return False

    def __call__(self,nice=False):
        self.start(nice =nice)

    def __del__(self):
        if exists(self._cwd):
            rmtree(self._cwd)
