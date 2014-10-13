import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

earth_file_dir = '../earth_model_nongravity/He50km_VisK5.0E17_VisM1.0E19/'
subflts_files = ['../fault_model/subflts_rake90/flt_0015']

stdout = open('stdout','wt')
cmd = ComputeGreensFunction(
    epochs = [1200],
    file_sites = 'stations.in',
    earth_file = join(earth_file_dir, 'earth.model_He50km_VisK5.0E17_VisM1.0E19'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    stdout = stdout
    )

if __name__ == '__main__':
    cmd()
    stdout.close()
