import glob
from os.path import basename

from viscojapan.pollitz.pollitz_wrapper import stat2gA

subflts_files = \
              sorted(glob.glob('subflts/flt_????'))

com = ComputeGreensFunction(
    epochs = [0],
    file_sites = 'sites_with_seafloor',
    earth_file = 'earth_model/earth.model_He50km',
    earth_file_dir = 'earth_model/earth_files/',
    outputs_dir = 'outs',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    G_file = 'G.h5'
    )
com.run()
