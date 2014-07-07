from os.path import exists,join,basename, dirname
from os import makedirs
from subprocess import Popen, check_output
from tempfile import mkdtemp
from shutil import copyfile, rmtree
import warnings

from ...utils import delete_if_exists, create_dir_if_not_exists


class PollitzWrapper(object):
    def __init__(self,
                 input_files = {},
                 output_files = {},
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 cwd = None,
                 if_keep_cwd = False
                 ):
        '''
"input_files" and "output_files" format:
    file_target : file_real
'''
        self.input_files = input_files        
        self.output_files = output_files

        self.if_skip_on_existing_output = if_skip_on_existing_output
        
        self.stdout = stdout
        self.stderr = stderr     

        # Change cwd for the command. See Popen page.
        # cwd is a temporary directory.
        self._tmp_dir = '/home/zy/tmp/'
        self._set_cwd(cwd)
        self.if_keep_cwd = if_keep_cwd
        
        
        self._cmd = None

    def _check_input_files(self):
        for f_target, f_real in self.input_files.items():
            assert exists(f_real), "Input file %s doesn't not exist!"%f_real

    def _set_cwd(self, cwd):
        '''cwd == None - means temperary directory is used.'''
        if cwd is None:
            create_dir_if_not_exists(self._tmp_dir)
            self.cwd = mkdtemp(dir=self._tmp_dir)
        else:
            create_dir_if_not_exists(cwd)
            self.cwd = cwd
        
    def _deploy_working_directory(self):
        ''' Copy earth files to temporary working directory.
'''
        for f_target, f_real in self.input_files.items():
            copyfile(f_real, join(self.cwd, basename(f_target)))

    def _run_command(self, nice=False):
        assert self._cmd != None, "Assign command _cmd."
        cmd = []
        if nice:
            cmd = ['nice']
        cmd.append(self._cmd)
        with self.gen_stdin() as fin:
            Popen(cmd, stdout=self.stdout, stderr=self.stderr,
                  stdin=fin, cwd=self.cwd).wait()


    def _fetch_output_from_working_directory(self):
        for f_target, f_real in self.output_files.items():
            d_real = dirname(f_real)
            if d_real != '':
                create_dir_if_not_exists(d_real)
            # fetch output from the temp dir.
            copyfile(join(self.cwd, f_target),f_real)

    def _delete_working_directory(self):
        if not self.if_keep_cwd:
            if self.cwd is not None:
                delete_if_exists(self.cwd)

    def gen_stdin(self):
        raise NotImplementedError()

    def stdin_to_file(self, file_name):
        fout = open(file_name, 'wt')
        with self.gen_stdin() as fid:
            fout.write(fid.read())
        fout.close()

    def run(self,nice=False):
        ''' Start to run the program.
'''
        if self.if_skip_on_existing_output and self.if_outputs_exist():
            msg = "    Skipped! Outputs found: "
            for f_target, f_real in self.output_files.items():
                msg += '%s, '%f_target
            print(msg)
            #warnings.warn(msg)
            return

        self._check_input_files()    
        self._deploy_working_directory()        
        self._run_command(nice=nice)
        self._fetch_output_from_working_directory()
        self._delete_working_directory()
        
    def if_outputs_exist(self):
        '''If output file exists.
'''
        for f_target, f_real in self.output_files.items():
            if not exists(f_real):
                return False
        return True

    def __call__(self,nice=False):
        self.run(nice =nice)

    def __del__(self):
        self._delete_working_directory()
                 
    
