import numpy as np
import h5py

import viscojapan as vj

from epochs_log import epochs

if __name__ == '__main__':
    dd = vj.DeformationDecomposition(
        f_res = '../outs/nrough_10.h5',
        file_G0 = '../../green_function/G_He40km_Vis5.8E18_Rake81.h5',
        files_Gs = ['../../green_function/G_He40km_Vis1.1E19_Rake81.h5',
                    '../../green_function/G_He45km_Vis5.8E18_Rake81.h5',
                    '../../green_function/G_He40km_Vis5.8E18_Rake90.h5'
                    ],
        nlin_par_names = ['log10(visM)','He','rake'],
        sites_file = '../../sites_with_seafloor',
        epochs = epochs,
        )
    print('disp_cmpts/total')
    dd.gen_total_disp_file('disp_cmpts/total')
    print('elastic')
    dd.gen_elastic_file('disp_cmpts/elastic')
    print('Rco')
    dd.gen_co_relax_file('disp_cmpts/Rco')
    print('Raslip')
    dd.gen_aslip_relax_file('disp_cmpts/Raslip')
    
