from .decay4m import decay4m

__all__=['decay4']

class decay4(decay4m):
    ''' decay4
Determine characteristic decay times, for spheroidal motion. Non-gravitational program.
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
    
