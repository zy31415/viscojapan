import tempfile
from os.path import exists, join, dirname
from os import makedirs
import h5py

import numpy as np

import pGMT

from .utils import file_kur_top, file_etopo1
from .plot_slip_txt_file import GMTSlipPlotter
from ...fault_model import FaultFileReader
from ...inversion.result_file.result_file_reader import ResultFileReader
from ...moment import MomentCalculator
from ...utils import get_middle_point

__all__ = ['GMTInversionResultFileSlipPlotter']

def get_slip_results_for_gmt(res_file, fault_file):        
    reader = FaultFileReader(fault_file)
    lats = reader.LLats
    lons = reader.LLons

    lats_m = get_middle_point(lats)
    lons_m = get_middle_point(lons)

    reader = SlipResultReader(res_file, fault_file)

    
    slip = reader.get_3d_incr_slip()    

    _arr = np.array([lons_m.flatten(), lats_m.flatten(), slip.flatten()]).T

    return _arr

class GMTInversionResultFileSlipPlotter(GMTSlipPlotter):
    def __init__(self,
                 gplt,
                 result_file,
                 fault_file,
                 earth_file,
                 topo_file = file_etopo1,
                 workdir = '~tmp',
                 I = '5k',
                 low_cut_value = 1,
                 A = '-70/20'
                 ):
        self.result_file = result_file
        self.fault_file = fault_file
        self.earth_file = earth_file

        self._prepare_tmp_slip_file()
        
        super().__init__(
            gplt = gplt,
            slip_file_txt = self._tmp_slip_file_name,
            topo_file = file_etopo1,
            workdir = workdir,
            I = I,
            low_cut_value = low_cut_value,
            A = A)

    def _prepare_tmp_slip_file(self):
        _arr = get_slip_results_for_gmt(self.result_file, self.fault_file)

        self._tmp_slip_file_id = tempfile.NamedTemporaryFile('w+t')
        self._tmp_slip_file_name = self._tmp_slip_file_id.name
        np.savetxt(self._tmp_slip_file_name, _arr, "%f %f %f")
        self._tmp_slip_file_id.seek(0,0)

    def close_tmp_file(self):
        if self._tmp_slip_file_id is not None:
            self._tmp_slip_file_id.close()
        self._tmp_slip_file_id = None

    def __del__(self):
        self.close_tmp_file()

    def plot_mag_string(self, x, y):
        mo, mw = self.compute_moment()
        with tempfile.NamedTemporaryFile('w+t') as fid:
            fid.write('%f %f Mo = %e, Mw = %.3f'%(x, y, mo, mw))
            fid.seek(0,0)

            self.gplt.pstext(fid.name, K='', O='', N='', R='', J='')

    def compute_moment(self):
        with h5py.File(self.result_file) as fid:
            slip = fid['Bm'][...]
        com = MomentCalculator(self.fault_file, self.earth_file)
        mo, mw = \
            com.compute_moment(slip)
        return mo, mw

    def plot_legend(self):
        mo, mw = self.compute_moment()
        with tempfile.NamedTemporaryFile('w+t') as text:
            text.write('''#
# scale
B {cpt_file} 0.1 0.2 -Baf::/:m:
G 0.2
# Mo and Mw
L 8 - C Mo = {mo:.2E}    Mw = {mw:.2f}
'''.format(
    cpt_file = self.cpt_file,
    mo = mo,
    mw = mw
    ))
            text.seek(0,0)
            self.gplt.pslegend(
                text.name, R='', J='', O='', K='',
                F='+gazure1', C='0.04i/0.07i', L='1.2',
                D='143.5/35.2/4/1.5/BL'
                )
        
        
        
        


    

        
        
        
    
    
        

