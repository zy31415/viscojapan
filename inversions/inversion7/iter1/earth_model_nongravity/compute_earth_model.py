import os
from os.path import join
import argparse

from viscojapan.pollitz.pollitz_wrapper import stat0A
from viscojapan.fault_model import FaultFileIO
import viscojapan as vj

FNULL = open(os.devnull, 'w')

fid = FaultFileIO('../fault_model/fault_bott50km.h5')
fault_bottom_depth = fid.depth_bottom
fault_top_depth = fid.depth_top

# l_max ~= 2*pi*R/He
lmax = 801

cmd1={}
cmd2={}

def add_model(model_str, l_max):
    cmd1[model_str]= stat0A(
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

    cmd2[model_str] = vj.pollitz.ComputeEarthModelVISCO1DNonGravity(
        earth_file = join(model_str, 'earth.model_'+model_str),
        l_max = lmax,
        outputs_dir = model_str,
        if_skip_on_existing_output = True,
        stdout = FNULL,
        stderr = FNULL,
        )

add_model('He50km_VisK5.0E17_VisM1.0E19', lmax)
add_model('He50km_VisK6.0E17_VisM1.0E19', lmax)
add_model('He50km_VisK5.0E17_VisM2.0E19', lmax)
add_model('He55km_VisK5.0E17_VisM1.0E19', lmax)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute earth model.')
    parser.add_argument('model', type=str, nargs=1,
                        help='Compute earth model.',
                        )
    args = parser.parse_args()
    model = args.model[0]

    cmd1[model]()
    cmd2[model].run()
