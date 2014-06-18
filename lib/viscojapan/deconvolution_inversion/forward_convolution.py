from multiprocessing import Pool

from numpy import dot

from ..epochal_data.epochal_data import EpochalData

class ForwardConvolution(object):
    def __init__(self):
        self.file_G = None
        self.slip = None
        self.file_output = None

    def init(self):
        # G matrix
        self.G = EpochalData(self.file_G)

    def init_output_file(self):
        simu_disp = EpochalData(self.file_output)
        for key in 'sites', 'He', 'lmax', 'visK', 'visM', 'log10_visM':
            val = self.G.get_info(key)
            simu_disp.set_info(key, val)
        self.output = simu_disp

    def get_disp_at_one_epoch(self, epoch):
        T = self.slip(0).reshape([-1,1])
        D = dot(self.G(epoch),T)
        for jj in range(1, epoch):
            T = self.slip(jj) - self.slip(jj-1)
            T = T.reshape([-1,1])
            D += dot(self.G(epoch-jj),T)
        return D

    def add_one_epoch(self, epoch, verbose=True):
        if verbose:
            print('Adding epoch %d to file %s'%(epoch, self.file_output))
        D = self.get_disp_at_one_epoch(epoch)        
        self.output.set_epoch_value(epoch, D)

    def add_epochs(self, epochs, verbose = True):
        for epoch in epochs:
            self.add_one_epoch(epoch, verbose = verbose)

    def mp_add_epochs(self, epochs, num_processes, verbose=True):
        with Pool(processes = num_processes) as pool:
            pool.map(self.add_one_epoch, epochs)
        
        
    
