import sys
from os.path import join

from pylab import pcolor, savefig, close, colorbar, axis

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.fault.fault_file_reader import FaultFileReader
from viscojapan.inversion_test.checkerboard_slip import gen_checkerboard_slip,gen_checkerboard_slip2
from viscojapan.utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

def test_fault_file_reader():
    fault = FaultFileReader('/home/zy/workspace/viscojapan/faultmodel/fault.h5')

    m = fault.get_num_subflts_in_strike()
    n = fault.get_num_subflts_in_dip()

    assert m==25
    assert n==10

def test_gen_checkerboard_slip():
    res = gen_checkerboard_slip(25,10,3,2)
    pcolor(res)
    colorbar()
    axis('equal')
    savefig(join(this_script_dir,'checker_board.pdf'))
    close()
