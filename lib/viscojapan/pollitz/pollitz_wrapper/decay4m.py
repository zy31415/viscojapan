from tempfile import TemporaryFile

from .pollitz_wrapper import PollitzWrapper

__all__=['decay4m','decay4']

class decay4m(PollitzWrapper):
    ''' decay4m
Determine characteristic decay times, for spheroidal motion
Output file: decay4.out
'''
    def __init__(self,
                 earth_model = None,
                 decay4_out = 'decay4.out',
                 l_min = None,
                 l_max = None,
                 
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):

        self.l_min = l_min
        self.l_max = l_max
        
        super().__init__(
            input_files = {'earth.model':earth_model},
            output_files = {'decay4.out':decay4_out},
            
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )
        self._cmd = 'decay4m'

    def gen_stdin(self):
        stdin=TemporaryFile('r+')
        stdin.write('%d  %d\n'%(self.l_min, self.l_max))
        stdin.seek(0)
        return stdin

class decay4(decay4m):
    ''' decay4m
Determine characteristic decay times, for spheroidal motion
Output file: decay4.out
'''
    def __init__(self,
                 earth_model = None,
                 decay4_out = 'decay4.out',
                 l_min = None,
                 l_max = None,
                 
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):
        super().__init__(
            earth_model = earth_model,
            decay4_out = decay4_out,
            l_min = l_min,
            l_max = l_max,
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,)
        
        self._cmd = 'decay4'
    
