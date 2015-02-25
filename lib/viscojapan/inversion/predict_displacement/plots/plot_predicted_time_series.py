from pylab import plt
import numpy as np

#from .pred_disp_database import PredDispToDatabaseReader
from viscojapan.inversion.predict_displacement.deformation_partition_file_reader import DeformPartitionResultReader
from viscojapan.tsana.observation_database import ObservationDatatbaseReader
from viscojapan.sites_db import get_site_true_name
from viscojapan.inversion.result_file import ResultFileReader

from date_conversion import adjust_mjd_for_plot_date

__all__ = ['PredictedTimeSeriesPlotter']

def calculate_lim(y, percentage=.2):
    y = np.asarray(y, float)
    y = np.nan_to_num(y)
    y2 = np.amax(y)
    y1 = np.amin(y)
    dy = y2 - y1
    return y1 - percentage*dy, y2 + percentage*dy

def shift_t(t):
    return np.asarray(t, int)+55631+adjust_mjd_for_plot_date

def regularize_y(ys):
    ys = np.asarray(ys, float)
    ys = np.nan_to_num(ys)
    return ys

class PredictedTimeSeriesPlotter(object): #TODO: this class is not coherent and can be break into three.
    def __init__(self,
                 partition_file,
                 result_file = None,
                 ):
        self.partition_file = partition_file
        reader = DeformPartitionResultReader(self.partition_file)
        self.Rco = reader.Rco
        self.Ecumu = reader.Ecumu
        self.Raslip = reader.Raslip
        self.d_added = reader.d_added

        if result_file is not None:
            reader = ResultFileReader(result_file)
            self.d_pred_from_result_file = reader.get_pred_disp()

        self.plt = plt

        self.obs_db = '/home/zy/workspace/viscojapan/tsana/db/~observation.db'
        self.obs_reader = ObservationDatatbaseReader(self.obs_db)
        
    def plot_cumu_disp_pred_from_result_file(self, site, cmpt, color='red', lw=2, **kwargs):
        ys = self.d_pred_from_result_file.cumu_ts(site, cmpt)
        ts = self.d_pred_from_result_file.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), '--', lw=lw, ms=2*lw, color=color, **kwargs)
        return list(ys)

    def plot_cumu_disp_pred_added(self, site, cmpt, color='red', lw=2, label=None, **kwargs):
        ys = self.d_added.cumu_ts(site, cmpt)
        ts = self.d_added.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), '-o', lw=lw, ms=2*lw,
                      color=color, label=label,
                      **kwargs)
        return list(ys)

    def plot_post_disp_pred_added(self, site, cmpt, color='red', lw=2, label=None, **kwargs):
        ys = self.d_added.post_ts(site, cmpt)
        ts = self.d_added.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), '-o', lw=lw, ms=2*lw,
                      color=color, label=label,
                      **kwargs)
        return list(ys)

    def plot_cumu_obs_linres(self, site, cmpt,label='obs.', **kwargs):
        ts, ys = self.obs_reader.get_cumu_obs_linres(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), 'x', ms=5, label=label, **kwargs)

    def plot_R_co(self, site, cmpt,
                  style = '-^', lw=1, **kwargs):
        ys = self.Rco.post_ts(site, cmpt)
        ts = self.Rco.get_epochs()

        plt.plot_date(shift_t(ts), regularize_y(ys), style, lw=lw, ms = 4*lw, **kwargs)
        return list(ys)

    def plot_post_disp_pred_from_result_file(self, site, cmpt, color='red', lw=1, **kwargs):
        ys = self.d_pred_from_result_file.post_ts(site, cmpt)
        ts = self.d_pred_from_result_file.get_epochs()
        ys = np.asarray(regularize_y(ys), float)
        ys = np.nan_to_num(ys)
        plt.plot_date(shift_t(ts), regularize_y(ys), '--', lw=lw, ms=3*lw, color=color, **kwargs)
        return list(ys)
    
    def plot_post_obs_linres(self, site, cmpt, **kwargs):
        ts, ys = self.obs_reader.get_post_obs_linres(site, cmpt)
        ys = np.asarray(regularize_y(ys), float)
        ys = np.nan_to_num(ys)
        plt.plot_date(shift_t(ts), regularize_y(ys), 'x', **kwargs)
        return list(ys)

    def plot_E_cumu_slip(self, site, cmpt,
                         lw=1, ms = 7,
                         label='E',**kwargs):
        ys = self.Ecumu.cumu_ts(site, cmpt)
        ts = self.Ecumu.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), '-+', lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_E_aslip(self, site, cmpt,
                     lw=1, ms=7,
                     label='Easlip',**kwargs):
        ys = self.Ecumu.post_ts(site, cmpt)
        ts = self.Ecumu.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), '-+', lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_R_aslip(self, site, cmpt,
                     ls='-', marker='o',
                     lw=1, ms=2, label='Raslip',**kwargs):
        ys = self.Raslip.post_ts(site, cmpt)
        ts = self.Raslip.get_epochs()
        plt.plot_date(shift_t(ts), regularize_y(ys), ls=ls, marker=marker, lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_cumu_disp_decomposition(self, site, cmpt, loc=2, leg_fs=7,
                       if_ylim=False
                       ):        
        self.plot_cumu_obs_linres(site, cmpt)
        y = self.plot_cumu_disp_pred_added(site, cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style='-^', label='Rco', color='orange')
        y += self.plot_E_cumu_slip(site, cmpt, color='green')
        y += self.plot_R_aslip(site, cmpt, color='black')
        
        plt.grid('on')
        if if_ylim:
            plt.ylim(calculate_lim(y))

        plt.ylabel(r'm')
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.gcf().autofmt_xdate()
        plt.title('Cumulative Disp.: {site} - {cmpt}'.format(
            site = get_site_true_name(site_id=site),
            cmpt = cmpt
            ))

    def plot_post_disp_decomposition(self, site, cmpt, loc=2, leg_fs=7,
                       marker_for_obs = 'x',
                       ):
        y = self.plot_post_obs_linres(site,cmpt, label='obs.', marker=marker_for_obs)
        y += self.plot_post_disp_pred_added(site,cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style = '-^', label='Rco', color='orange')
        y += self.plot_E_aslip(site, cmpt, color='green')
        y += self.plot_R_aslip(site, cmpt, color='black')

        plt.grid('on')
        
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.ylabel(r'm')
        plt.gcf().autofmt_xdate()
        plt.title('Postseismic Disp. : {site} - {cmpt}'.format(
            site = get_site_true_name(site_id = site),
            cmpt = cmpt
            ))


    
 
