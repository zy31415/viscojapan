from viscojapan.pollitz.pollitz_wrapper import stat0A

cmd = stat0A(
    earth_model_stat = 'earth.model_He50km',
    stat0_out = 'earth_files/stat0.out',
    l_min = 1,
    l_max = 15000,
    fault_bottom_depth = 50.,
    fault_top_depth = 3.,
    obs_dep = 0.,
    if_skip_on_existing_output = True,
    stdout = open('/dev/null', 'w')
    )

cmd()


cmd = ComputeEarthModelVISCO1D(
    earth_file = 'earth.model_He50km',
    l_max = 810,
    outputs_dir = 'earth_files',
    if_skip_on_existing_output = True,
    stdout = None,
    stderr = None,
    )

cmd()
