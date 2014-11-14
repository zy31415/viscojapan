import subprocess
import tempfile
import shutil

def _check_return_code(return_code, error_message):
    if return_code != 0:
        raise Exception(error_message)

def _form_gmt_escape_shell_command(command, args, kwargs):
    out = ['gmt', command]
    out += args
    for k, v in kwargs.items():
        if v is not None:
            if k == 'eq':
                arg = '= {v}'.format(v=v)
            else:
                arg = '-{k}{v}'.format(k=k,v=v)
            out.append(arg)            
                
    return out

class GMT(object):
    def __init__(self):
        self._tmp_stdout = tempfile.NamedTemporaryFile()
        self._tmp_stderr = tempfile.NamedTemporaryFile(mode='w+t')
        

    def __getattr__(self, command):
        def f(*args, **kwargs):
            return self._gmtcommand(command, *args, **kwargs)
        return f

    def _gmtcommand(self, command, 
                          *args,
                          **kwargs):
        popen_args = _form_gmt_escape_shell_command(command, args, kwargs)
        p = subprocess.Popen(
            ' '.join(popen_args),
            stdout = self._tmp_stdout,
            stderr = self._tmp_stderr,
            shell = True
            )
        
        return_code = p.wait()

        if return_code != 0:
            self._tmp_stderr.seek(0,0)
            print(self._tmp_stderr.read())
            raise Exception(
                'Command %s returned an error. While executing command:\n%s'%\
                           (command, popen_args))

    def __del__(self):
        try:
            self._tmp_stdout.close()
        except:
            pass

    def save_stdout(self, filename):
        self._tmp_stdout.seek(0,0)
        with open(filename, 'wb') as fid:
            shutil.copyfileobj(self._tmp_stdout, fid)

    def save_stderr(self, filename):
        self._tmp_stderr.seek(0,0)
        with open(filename, 'wb') as fid:
            shutil.copyfileobj(self._tmp_stdout, fid)
        
        
