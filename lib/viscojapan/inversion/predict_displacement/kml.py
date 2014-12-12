from os.path import exists
from os import makedirs

import simplekml

import numpy as np

from ...sites_db import get_pos_dic
from .plot_predicted_time_series import PredictedTimeSeriesPlotter

class KMLShowTimeSeries(object):
    def __init__(self,
                 file_sites,
                 db_pred,
                 ):
        self.file_sites = file_sites
        sites = np.loadtxt(self.file_sites, '4a', usecols=(0,))
        self.sites = [site.decode() for site in sites]
        
        self.db_pred = db_pred
        self.dir_plots = 'plots/'

    def plot(self):
        if not exists(self.dir_plots):
            makedirs(self.dir_plots)
            
        plt = PredictedTimeSeriesPlotter(self.db_pred)

        loc = 2
        leg_fs = 6

        for site in self.sites:
            print(site)
            for cmpt in 'e', 'n', 'u':        
                plt.plot_cumu_obs_linres(site, cmpt, label='obs.')
                plt.plot_cumu_disp_pred(site, cmpt, label='pred.')
                plt.plt.legend(loc=loc, prop={'size':leg_fs})
                plt.plt.title('%s-%s'%(site, cmpt))
                plt.plt.savefig('plots/%s.%s.cumu.png'%(site, cmpt))
                plt.plt.close()

                plt.plot_post_obs_linres(site,cmpt, label='obs.')
                plt.plot_post_disp_pred(site,cmpt, label='pred.')
                plt.plt.legend(loc=loc, prop={'size':leg_fs})
                plt.plt.title('%s-%s'%(site, cmpt))
                plt.plt.savefig('plots/%s.%s.post.png'%(site, cmpt))
                plt.plt.close()      
        
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
]]>
'''.format(site=site)
                        
        kml.save("time_series.kml")
