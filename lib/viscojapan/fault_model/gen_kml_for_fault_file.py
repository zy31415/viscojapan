import simplekml as sk
import numpy as np

from .fault_file_io import FaultFileReader

__all__ = ['gen_kml_for_fault_file']

def gen_kml_for_fault_file(fault_file, kml_file):
    with FaultFileReader(fault_file) as reader:
        lons = reader.LLons
        lats = reader.LLats

    kml = sk.Kml()
    ls = kml.newlinestring(name='Fault Grids')

    coords = []
    for lati, loni in zip(np.nditer(lats),
                          np.nditer(lons)):
        coords.append([lati, loni, 10.])
    ls.coords = coords
    ls.extrude = 1
    ls.altitudemode = sk.AltitudeMode.relativetoground
    kml.save(kml_file)
        
    
