import glob

from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction

from epochs import epochs

subflts_files = \
              sorted(glob.glob('../fault_model/subflts/flt_????'))

com = ComputeGreensFunction(
    epochs = epochs[0:],
    file_sites = 'sites_with_seafloor',
    earth_file = '../earth_model/earth.model_He50km',
    earth_file_dir = '../earth_model/earth_files/',
    outputs_dir = 'outs',
    subflts_files = subflts_files,
    controller_file = 'pool.config',
    )

if __name__ == '__main__':
    com.run()
