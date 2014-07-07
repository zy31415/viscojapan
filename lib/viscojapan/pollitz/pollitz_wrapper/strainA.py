from tempfile import TemporaryFile

from date_conversion.date_conversion import asdyr

from .pollitz_wrapper import PollitzWrapper
from .utils import read_flt_file_for_stdin, read_sites_file_for_stdin

class strainA(PollitzWrapper):
    ''' strainA
Determine spheroidal motion eigenfunctions
Input file: 'earth.model','decay.out','decay4.out',
            'vsph.out','vtor.out'
Output file: out
'''
    def __init__(self,
                 earth_model = None,
                 decay_out = None,
                 decay4_out = None,
                 vsph_out = None,
                 vtor_out = None,

                 file_flt=None, # faults file
                 file_sites=None, # sites file
                 days_after = None,

                 file_out=None, # output file
                
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):

        self.file_flt = file_flt
        self.file_sites = file_sites
        self.file_out = file_out
        self.days_after = days_after

        self.t_eq = 55631 
        
        super().__init__(
            input_files = {'earth.model':earth_model,
                           'decay.out' :decay_out,
                           'decay4.out':decay4_out,
                           'vsph.out' : vsph_out,
                           'vtor.out' : vtor_out
                           },
            output_files = {'out':file_out},
            
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,
            )
        self._cmd = 'strainA'

    def gen_stdin(self):
        ''' Form the stdin for command strainA.
'''
        t1 = asdyr(self.t_eq)
        t2 = asdyr(self.t_eq+self.days_after)
        # temporary file:
        stdin=TemporaryFile('r+')
        stdin.write('Comment Line.\n')
        stdin.write(read_flt_file_for_stdin(self.file_flt, 'head'))
        stdin.write("%f %f %f 1.\n"%(t1,t1,t2))
        stdin.write(read_flt_file_for_stdin(self.file_flt, 'body'))
        stdin.write(read_sites_file_for_stdin())
        stdin.write("0\n")
        stdin.write("0\n")
        stdin.write("out\n")
        stdin.seek(0)
        return stdin

    
        
    
