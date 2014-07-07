from tempfile import TemporaryFile

from .pollitz_wrapper import PollitzWrapper

class decay(PollitzWrapper):
    ''' decay
Determine characteristic decay times, for troidal motion
Output file: decay.out
'''
    def __init__(self,
                 earth_model = None,
                 decay_out = 'decay.out',
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
            output_files = {'decay.out':decay_out},
            
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )
        self._cmd = 'decay'

    def gen_stdin(self):
        stdin=TemporaryFile('r+')
        stdin.write('%d  %d\n'%(self.l_min, self.l_max))
        stdin.seek(0)
        return stdin
    
