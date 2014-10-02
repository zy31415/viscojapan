from tempfile import TemporaryFile

from .pollitz_wrapper import PollitzWrapper

__all__ = ['vsphm','vsphdep']

class vsphm(PollitzWrapper):
    ''' vsphm
Determine spheroidal motion eigenfunctions
Input file: decay4.out
Output file: vsph.out
'''
    def __init__(self,
                 earth_model = None,
                 decay4_out = None,
                 vsph_out = 'vsph.out',
                 obs_dep = 0.0,
                 
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):

        self.obs_dep = obs_dep
        
        super().__init__(
            input_files = {'earth.model':earth_model,
                           'decay4.out':decay4_out},
            output_files = {'vsph.out':vsph_out},
            
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )
        self._cmd = 'vsphm'

    def gen_stdin(self):
        stdin=TemporaryFile('r+')
        stdin.write('%f \n'%(self.obs_dep))
        stdin.seek(0)
        return stdin

class vsphdep(vsphm):
    ''' vsphdep
Determine spheroidal motion eigenfunctions
Input file: decay4.out
Output file: vsph.out
'''
    def __init__(self,
                 earth_model = None,
                 decay4_out = None,
                 vsph_out = 'vsph.out',
                 obs_dep = 0.0,
                 
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):
        super().__init__(
            earth_model = earth_model,
            decay4_out = decay4_out,
            vsph_out = vsph_out,
            obs_dep = obs_dep,
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,)
        self._cmd = 'vsphdep'    
