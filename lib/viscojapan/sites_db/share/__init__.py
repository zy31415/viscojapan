from os.path import join

from ...utils import get_this_script_dir

__all__ = ['file_gps_sites_db']

this_script_dir = get_this_script_dir(__file__)

file_gps_sites_db = join(this_script_dir, 'gps_sites.sqlite3')
