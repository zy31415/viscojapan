import subprocess

def _check_return_code(return_code, error_message):
    if return_code != 0:
        raise Exception(error_message)

def _form_gmt_escape_shell_command(command, args, kwargs):
    out = ['gmt', command]
    out += args
    for k, v in kwargs.items():
        out.append('-{k}{v}'.format(k=k,v=v))
    return out

class GMT(object):
    def __init__(self):
        self._tmp_stdout = subprocess.PIPE

    def __getattr__(self, command):
        def f(*args, **kwargs):
            return self._gmtcommand(command, *args, **kwargs)
        return f

    def _gmtcommand(self, command, 
                          *args,
                          **kwargs):
        popen_args = _form_gmt_escape_shell_command(command, args, kwargs)
        p = subprocess.Popen(
            popen_args,
            stdout = self._tmp_stdout
            )
        
        return_code = p.wait()

        _check_return_code(return_code,
                           'Command %s returned an error. While executing command:\n%s'%\
                           (command, popen_args))
