import simplekml as sk
import numpy as np

from .fault_file_reader import FaultFileReader

__all__ = ['gen_kml_for_fault_file']

def _new_lines_string(kml, lons, lats, name=None):
    ls = kml.newlinestring(name=name)
    coords = []
    for lati, loni in zip(np.nditer(lats),
                          np.nditer(lons)):
        coords.append([loni, lati])
    ls.coords = coords
    ls.extrude = 1
    ls.altitudemode = sk.AltitudeMode.relativetoground

def gen_kml_for_fault_file(fault_file, kml_file):
    with FaultFileReader(fault_file) as reader:
        lons = reader.LLons
        lats = reader.LLats
    kml = sk.Kml()
    # plot each row
    for loni, lati in zip(lons, lats):
        _new_lines_string(kml, loni, lati)
    # plot each column
    for loni, lati in zip(lons.T, lats.T):
        _new_lines_string(kml, loni, lati)
    kml.save(kml_file)
        
    
