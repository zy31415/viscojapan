from os.path import join

from ...utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

raw_file_He33km = join(this_script_dir, 'earth.modelBURG-SUM_33km')
raw_file_He40km = join(this_script_dir, 'earth.modelBURG-SUM_40km')
raw_file_He45km = join(this_script_dir, 'earth.modelBURG-SUM_45km')
raw_file_He46km = join(this_script_dir, 'earth.modelBURG-SUM_46km')
raw_file_He50km = join(this_script_dir, 'earth.modelBURG-SUM_50km')
raw_file_He51km = join(this_script_dir, 'earth.modelBURG-SUM_51km')
raw_file_He55km = join(this_script_dir, 'earth.modelBURG-SUM_55km')
raw_file_He60km = join(this_script_dir, 'earth.modelBURG-SUM_60km')
raw_file_pollitz_He63km = join(this_script_dir, 'earth.modelBURG-SUM_pollitz_63km')
raw_file_He63km = raw_file_pollitz_He63km

__all__ = ['raw_file_He33km','raw_file_He40km',
           'raw_file_He45km','raw_file_He46km','raw_file_He50km',
           'raw_file_He51km',
           'raw_file_He55km','raw_file_He60km',
           'raw_file_He63km',
           'raw_file_pollitz_He63km']
