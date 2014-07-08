from viscojapan.pollitz.compute_greens_function import ComputeGreensFunction

com = ComputeGreensFunction(
    fault_file = 'share/fault.h5',
    earth_file = 'share/earth.model_He50km',
    sites_file = 'share/sites_with_seafloor',
    l_max_static = 3,
    controller_file = 'pool.config')

com.go()
