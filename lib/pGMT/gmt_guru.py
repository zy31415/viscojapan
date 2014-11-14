import subprocess

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

class GMTGuru(object):
    def __init__(self):
        self.stderr = None
        self.stdout = None


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
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
            )
        self.stdout, self.stderr = p.communicate()
        
        if p.returncode != 0:
            print(self.stderr.decode())
            raise Exception(
                'Command %s returned an error. While executing command:\n%s'%\
                           (command, popen_args))
