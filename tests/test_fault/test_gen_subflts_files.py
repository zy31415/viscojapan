from os.path import join

from viscojapan.fault.gen_subflt_files import gen_subflts_files
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

def test():
    gen_subflts_files(join(this_test_path, 'subfaults.h5'), '~outs')
