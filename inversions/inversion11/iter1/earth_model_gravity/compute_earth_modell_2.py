import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.fault_model import FaultFileReader
import viscojapan as vj

FNULL = open(os.devnull, 'w')

fid = FaultFileReader('../fault_model/fault_bott80km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

# l_max ~= 2*pi*R/He
lmax = 850

cmd1={}
cmd2={}

def add_model(model_str, l_max, model_num):
    cmd1['%d'%model_num]= stat0A(
        earth_model_stat = join(model_str, 'earth.model_'+model_str),
        stat0_out = join(model_str, 'stat0.out'),
        l_min = 1,
        l_max = 15000,
        fault_bottom_depth = fault_bottom_depth,
        fault_top_depth = fault_top_depth,
        obs_dep = 0.,
        if_skip_on_existing_output = True,
        stdout = FNULL
        )

    cmd2['%d'%model_num] = vj.pollitz.ComputeEarthModelVISCO1D(
        earth_file = join(model_str, 'earth.model_'+model_str),
        l_max = lmax,
        outputs_dir = model_str,
        if_skip_on_existing_output = True,
        stdout = FNULL,
        stderr = FNULL,
        )

add_model('He50km_VisM9.5E18', lmax, 0)
add_model('He50km_VisM9.0E18', lmax, 1)
add_model('He50km_VisM8.5E18', lmax, 2)
add_model('He50km_VisM8.0E18', lmax, 3)
add_model('He50km_VisM7.5E18', lmax, 4)
add_model('He50km_VisM7.0E18', lmax, 5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute earth model.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute earth model.',
                        )
    args = parser.parse_args()
    model = args.model[0]
    if model =='all':
        for c1, c2 in zip(cmd1, cmd2):
            cmd1[c1]()
            cmd2[c2].run()
    else:
        cmd1[model]()
        cmd2[model].run()
