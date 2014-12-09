import numpy as np

from .result_file_reader import ResultFileReader

__all__ = ['collect_from_result_files']

def collect_from_result_files(files, prop):
    outs = []
    for file in files:        
        with ResultFileReader(file) as reader:
            outs.append(getattr(reader,prop))
    return np.asarray(outs, float)
            

    
    
