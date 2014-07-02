import h5py

class FaultFileIO(object):
    def __init__(self, fault_file):
        self.fault_file = fault_file

    def get_num_subflts_in_strike(self):
        with h5py.File(self.fault_file, 'r') as fid:
            num_subflts_in_strike = fid['num_subflts_in_strike'][...]
        return num_subflts_in_strike
            

    def get_num_subflts_in_dip(self):
        with h5py.File(self.fault_file, 'r') as fid:
            num_subflts_in_dip = fid['num_subflts_in_dip'][...]
        return num_subflts_in_dip

    

    
        
