from tempfile import TemporaryFile

from .pollitz_wrapper import PollitzWrapper

class vtordep(PollitzWrapper):
    ''' vtordep
Determine toroidal motion eigenfunctions
Input file: decay.out
Output file: vtor.out
'''
    def __init__(self,
                 earth_model = None,
                 decay_out = 'decay.out',
                 vtor_out = 'vtor.out',
                 obs_dep = 0.0,
                 
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):

        self.obs_dep = obs_dep
        
        super().__init__(
            input_files = {'earth.model':earth_model,
                           'decay.out':decay_out},
            output_files = {'vtor.out':vtor_out},
            
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )
        self._cmd = 'vtordep'

    def gen_stdin(self):
        stdin=TemporaryFile('r+')
        stdin.write('%f \n'%(self.obs_dep))
        stdin.seek(0)
        return stdin
    
