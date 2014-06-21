from numpy import hstack
from numpy.random import normal

def gen_error_for_sites(num_sites,
                        east_st=6e-3, north_st=6e-3, up_st=20e-3):
    east_error = normal(0, east_st, (num_sites,1))
    north_error = normal(0, north_st, (num_sites,1))
    up_error = normal(0, up_st, (num_sites,1))
    error = hstack((east_error, north_error, up_error))
    error_flat = error.flatten().reshape([-1,1])
    return error_flat
