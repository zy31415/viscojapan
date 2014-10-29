from fault_file_io import FaultFileReader

def gen_kml_for_fault_file(fault_file):
    with FaultFileReader(fault_file) as reader:
        lons = reader.LLons
        lats = reader.LLats
        
    
