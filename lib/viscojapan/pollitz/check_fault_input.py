from os.path import join
import glob

from numpy import asarray, ones_like
from numpy.testing import assert_array_equal

from viscojapan.pollitz.parse_fault_input import parse_fault_input
from viscojapan.plots import MapPlot, plt, MapPlotSlab, MapPlotFault
from viscojapan.fault_model import FaultFileIO
from viscojapan.test_utils import MyTestCase

class CheckSubfaultsInput(object):
    def setUp(self):
        self.subflts_dir = None
        self.original_fault_file = None

    def _get_fault_shape(self):
        fio = FaultFileIO(self.original_fault_file)
        return (fio.num_subflt_along_dip, fio.num_subflt_along_strike)
    
    def iterate_files(self):
        for fn in sorted(glob.glob(join(self.subflts_dir, 'flt_????'))):
            yield fn

    def read_pars(self,name):
        outs = []
        for fn in self.iterate_files():
            res = parse_fault_input(fn)[name]
            if hasattr(res, '__len__'):
                assert len(res)==1
                res = res[0]
            outs.append(res)
        return asarray(outs)

    def plot_original_fault(self):
        MapPlotFault(fault_file = self.original_fault_file).plot_fault()
        
    def test_lonlat_grids(self):
        lons = self.read_pars('lons')
        lats = self.read_pars('lats')

        self.plot_original_fault()

        mplt = MapPlot()
        mplt.basemap.plot(lons,lats,
                          latlon=True,marker='.', ls='', color='red')

        MapPlotSlab().plot_top()
        plt.savefig(join(self.outs_dir, 'lonlat.png'))
        plt.close()

    def test_slip(self):
        slips = self.read_pars('slips')
        assert_array_equal(slips, ones_like(slips))

    def test_dep_top(self):
        dips = self.read_pars('top')
        MapPlotFault(fault_file = self.original_fault_file).pcolor_on_fault(dips)
        plt.title('top')
        plt.savefig(join(self.outs_dir, 'dep_top.png'))
        plt.close()

    def test_dep_bottom(self):
        dips = self.read_pars('bottom')
        MapPlotFault(fault_file = self.original_fault_file).plot_slip(dips.reshape([-1,1]))
        plt.title('bottom')
        plt.savefig(join(self.outs_dir, 'dep_bottom.png'))
        plt.close()

    def test_rake(self):
        rakes = self.read_pars('rakes')
        assert_array_equal(rakes, ones_like(rakes)*90.)
        
    def test_strike(self):
        strikes = self.read_pars('strikes')
        fio = FaultFileIO(self.original_fault_file)
        assert_array_equal(strikes,
                           ones_like(strikes)*fio.flt_strike)
        
    def test_dip(self):
        dips = self.read_pars('dip')
        MapPlotFault(fault_file = self.original_fault_file).plot_slip(dips.reshape([-1,1]))
        plt.title('dip')
        plt.savefig(join(self.outs_dir, 'dip.png'))
        plt.close()
    
    def test_flt_length(self):
        strikes = self.read_pars('strikes')
        fio = FaultFileIO(self.original_fault_file)
        assert_array_equal(strikes,
                           ones_like(strikes)*fio.flt_strike)
