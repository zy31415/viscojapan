from viscojapan.pollitz.pollitz_wrapper import stat2gA

cmd = stat2gA(
    earth_model_stat = 'share/earth.model_He50km',
    stat0_out = 'workspace/stat0.out',
    file_flt = 'share/subflts/flt_0000',
    file_sites = 'share/sites_with_seafloor',
    file_out = 'outs_disp/out1',
    if_skip_on_existing_output = True,
    )

cmd()
