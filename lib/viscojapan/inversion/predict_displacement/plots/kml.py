from os.path import exists, join
from os import makedirs
from multiprocessing import Pool

import simplekml
import numpy as np

from ....sites_db import get_pos_dic
from .plot_predicted_time_series import PredictedTimeSeriesPlotter
from .plot_predicted_velocity_time_series import PredictedVelocityTimeSeriesPlotter


class KMLShowTimeSeries(object): #TODO: add (1)if plot prediction from the result file (2) if check addded and predicted
    def __init__(self,
                 file_sites,
                 result_file,
                 partition_file,
                 if_overwrite = False
                 ):
        self.file_sites = file_sites
        sites = np.loadtxt(self.file_sites, '4a', usecols=(0,))
        self.sites = [site.decode() for site in sites]
        
        self.partition_file = partition_file
        self.result_file = result_file
        self.dir_plots = 'plots/'
        self.if_overwrite = if_overwrite

    def plot_site(self, site, file_ext):
        if not exists(self.dir_plots):
            makedirs(self.dir_plots)

        plt = PredictedTimeSeriesPlotter(
            partition_file = self.partition_file,
            result_file = self.result_file
        )

        plt_vel = PredictedVelocityTimeSeriesPlotter(
            partition_file = self.partition_file
        )
        
        print(site)
        
        for cmpt in 'e', 'n', 'u':
            fn = join(self.dir_plots, '%s.%s.cumu.%s'%(site, cmpt, file_ext))
            if (self.if_overwrite) or (not exists(fn)):
                plt.plot_cumu_disp_decomposition(site, cmpt)
                plt.plt.savefig(fn)
                plt.plt.close()

            fn = join(self.dir_plots, '%s.%s.post.%s'%(site, cmpt, file_ext))
            if (self.if_overwrite) or (not exists(fn)):
                plt.plot_post_disp_decomposition(site, cmpt)
                plt.plt.savefig(fn)
                plt.plt.close()

            fn = join(self.dir_plots, '%s.%s.vel.%s'%(site, cmpt, file_ext))
            if (self.if_overwrite) or (not exists(fn)):
                plt_vel.plot_vel_decomposition(site, cmpt)
                plt.plt.savefig(fn)
                plt.plt.close()

    def _plot_site_for_Pool(self, kwargs):
        self.plot_site(**kwargs)

    def plot(self, file_ext = 'png', nproc = 1):
        pool = Pool(processes = nproc)
        kwargs = [{'site':site, 'file_ext':file_ext} for site in self.sites]        
        pool.map(self._plot_site_for_Pool, kwargs)
        
    def save_kml(self, fn):        
        pos_dic = get_pos_dic()
        kml = simplekml.Kml()

        for site in self.sites:
            lon, lat = pos_dic[site]
            pnt = kml.newpoint(name=site, coords=[(lon,lat)])
            pnt.description = '''<![CDATA[
<h1>Predicted and observed coseismic + postseismic time series</h1>
<img src="plots/{site}.e.cumu.png">
<img src="plots/{site}.n.cumu.png">
<img src="plots/{site}.u.cumu.png">

<h1>Postseismic time series only</h1>
<img src="plots/{site}.e.post.png">
<img src="plots/{site}.n.post.png">
<img src="plots/{site}.u.post.png">

<h1>Predicted velocity time series</h1>
<img src="plots/{site}.e.vel.png">
<img src="plots/{site}.n.vel.png">
<img src="plots/{site}.u.vel.png">
]]>
'''.format(site=site)
                        
        kml.save("time_series.kml")
