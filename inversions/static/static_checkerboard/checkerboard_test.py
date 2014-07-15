from numpy import logspace

from viscojapan.inversion_test import CheckerboardTest

from viscojapan.plots import MapPlotFault, plt

f_G = '/home/zy/workspace/viscojapan/inversions/static_inversion/coseismic_inversion_b_spline/greens_function/G.h5'
f_fault = '/home/zy/workspace/viscojapan/inversions/static_inversion/coseismic_inversion_b_spline/fault_model/fault_He50km_east.h5'
filter_site_file = 'sites'
filter_site_seafloor_file = 'sites_with_seafloor'

if __name__ =='__main__':
    alphas = logspace(-4,0,30)
    test1 = CheckerboardTest(f_G,
                             filter_site_file = filter_site_seafloor_file,
                             fault_file = f_fault,
                             sd_horizontal = 0.006,
                             sd_up = 0.02,
                             dip_patch_size = 4,
                             strike_patch_size = 4,)

    test1.make_L_curve(alphas, 'plots_with_seafloor')

