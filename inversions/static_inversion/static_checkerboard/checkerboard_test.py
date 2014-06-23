from viscojapan.inversion_test import CheckerboardTest

f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
filter_site_file = 'sites'
filter_site_seafloor_file = 'sites_with_seafloor'

if __name__ =='__main__':
    alphas = logspace(-4,0,30)
    test1 = CheckerboardTest()
    test1.f_G = f_G
    test1.filter_site_file = filter_site_seafloor_file
    test1.make_L_curve(alphas, 'plots_with_seafloor')

    test2 = CheckerboardTest()
    test2.f_G = f_G
    test2.filter_site_file = filter_site_file
    test2.make_L_curve(alphas, 'plots')
