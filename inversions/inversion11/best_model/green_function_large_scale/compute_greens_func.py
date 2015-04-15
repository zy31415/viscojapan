import glob
import argparse
from os.path import join

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

epochs = epochs[1:] + [0]

subflts = \
        sorted(glob.glob('../fault_model/subflts/flt_????'))

earth_file_dir = '../earth_model_gravity/standard_model/'
cmd = ComputeGreensFunction(
    epochs = epochs,
    file_sites = 'stations_large_scale.in',
    earth_file = join(earth_file_dir, 'earth.model'),
    earth_file_dir = earth_file_dir,
    outputs_dir = 'outs/',
    subflts_files = subflts,
    controller_file = 'pool.config',
    )


if __name__ == '__main__':
    cmd()
