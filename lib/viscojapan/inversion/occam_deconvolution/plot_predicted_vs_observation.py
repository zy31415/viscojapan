import re

import numpy as np
from pylab import plt

from .occam_results_deformation_decomposition import read_predicted_time_series_from_results_file

__all__ = ['PlotPredictedVSObservation']

def set_axis(cmpt):
    plt.grid('on')
    plt.ylabel('%s/m'%cmpt)
    plt.xlim([0,1150])

class PlotPredictedVSObservation(object):
    def __init__(self,
                 site,
                 file_obs_cumu,
                 epochs,
                 file_pred_total,
                 file_pred_elastic,
                 file_pred_Rco,
                 file_pred_Raslip,
                 ):
        self.site = site
        self.file_obs_cumu = file_obs_cumu
        self.epochs = epochs
        self.file_pred_total = file_pred_total
        self.file_pred_elastic = file_pred_elastic
        self.file_pred_Rco = file_pred_Rco
        self.file_pred_Raslip = file_pred_Raslip
        
        t_obs, e_obs, n_obs, u_obs = self.read_observation()

    def read_observation(self):
        tp = np.loadtxt(self.file_obs_cumu)
        t = tp[:,0]
        y_obs_e = tp[:,1]
        y_obs_n = tp[:,2]
        y_obs_u = tp[:,3]

        return t, y_obs_e, y_obs_n, y_obs_u

    def plot_predicated_components(self, cmpt):    
        y_total = read_predicted_time_series_from_results_file(
            self.site, cmpt, self.file_pred_total)
        y_elastic = read_predicted_time_series_from_results_file(
            self.site, cmpt, self.file_pred_elastic)
        y_Rco = read_predicted_time_series_from_results_file(
            self.site, cmpt, self.file_pred_Rco)
        y_Raslip = read_predicted_time_series_from_results_file(
            self.site, cmpt, self.file_pred_Raslip)
        _y = y_elastic + y_Rco +  y_Raslip

        for y, label in zip((y_total, y_elastic, y_Rco, y_Raslip, _y),
                            ('total', 'elastic', r'$R_{\bf{co}}$', r'$R_{\bf{aslip}}$',
                             'total_')):
            #plt.semilogx(epochs,y,'o-', label=label)
            plt.plot(self.epochs,y,'o-', label=label)

    def plot(self):
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        t_obs, e_obs, n_obs, u_obs = self.read_observation()

        plt.sca(ax1)
        plt.title('%s'%(self.site))
        self.plot_predicated_components('e')
        plt.plot(t_obs, e_obs, '--', label='obs', color='black')
        set_axis('east')
        plt.legend(prop={'size':8}, bbox_to_anchor=(1.12,1.01))

        plt.sca(ax2)
        self.plot_predicated_components('n')
        plt.plot(t_obs, n_obs,'--', label='obs', color='black')
        set_axis('north')

        plt.sca(ax3)
        self.plot_predicated_components('u')
        plt.plot(t_obs, u_obs,'--', label='obs', color='black')
        plt.xlabel('days after the mainshock')
        set_axis('up')
        f.subplots_adjust(hspace=.1)

