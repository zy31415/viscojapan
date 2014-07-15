from multiprocessing import Pool

class ComputeLCurve(object):
    def __init__(self,
                 inversion,
                 args,
                 outputs_dir):
        self.inversion = inversion
        self.args = args
        self.outputs_dir = outputs_dir

    def invert(self, args):
        self.inversion.invert(*args)

    def run_mp(self, nproc):
        args = [arg for arg in zip(*self.args)]
        pool = Pool(nproc)
        pool.map(self.invert, args)
        
    
        
    
