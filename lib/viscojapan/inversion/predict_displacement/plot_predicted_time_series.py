from pylab import plt
import numpy as np

from .pred_disp_database import PredDispToDatabaseReader
from ...tsana.observation_database import ObservationDatatbaseReader
from ...sites_db import get_true_name_by_id

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

class PredictedTimeSeriesPlotter(object):
    def __init__(self,
                 pred_db,
                 ):
        self.pred_db = pred_db
        self.pred_reader = PredDispToDatabaseReader(self.pred_db)

        self.plt = plt

        self.obs_db = '/home/zy/workspace/viscojapan/tsana/db/~observation.db'
        self.obs_reader = ObservationDatatbaseReader(self.obs_db)
        
    def plot_cumu_disp_pred(self, site, cmpt, color='red', lw=2, **kwargs):
        ts, ys = self.pred_reader.get_cumu_disp_pred(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), '-o', lw=lw, ms=2*lw, color=color, **kwargs)
        return list(ys)

    def plot_cumu_disp_pred_added(self, site, cmpt, color='green', lw=1, **kwargs):        
        ts, ys = self.pred_reader.get_cumu_disp_added(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), '--', lw=lw, ms=2*lw,
                      color=color, label='cumulative disp. prediction added',
                      **kwargs)
        return list(ys)

    def plot_post_disp_pred_added(self, site, cmpt, color='green', lw=1, **kwargs):        
        ts, ys = self.pred_reader.get_post_disp_added(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), '--', lw=lw, ms=2*lw,
                      color=color, label='postseismic disp. prediction added',
                      **kwargs)
        return list(ys)

    def plot_cumu_obs_linres(self, site, cmpt,label='obs.', **kwargs):
        ts, ys = self.obs_reader.get_cumu_obs_linres(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), 'x', ms=5, label=label, **kwargs)

    def plot_R_co(self, site, cmpt,
                  style = '-^', lw=1, **kwargs):
        ts, ys = self.pred_reader.get_R_co(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), style, lw=lw, ms = 4*lw, **kwargs)
        return list(ys)

    def plot_post_disp_pred(self, site, cmpt, color='red', lw=2.5, **kwargs):
        ts, ys = self.pred_reader.get_post_disp_pred(site, cmpt)
        ys = np.asarray(regularize_y(ys), float)
        ys = np.nan_to_num(ys)
        plt.plot_date(shift_t(ts), regularize_y(ys), '-o', lw=lw, ms=3*lw, color=color, **kwargs)
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
        ts, ys = self.pred_reader.get_E_cumu_slip(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), '-+', lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_E_aslip(self, site, cmpt,
                     lw=1, ms=7,
                     label='Easlip',**kwargs):
        ts, ys = self.pred_reader.get_E_aslip(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), '-+', lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_R_aslip(self, site, cmpt,
                     ls='-', marker='o',
                     lw=1, ms=2, label='Raslip',**kwargs):
        ts, ys = self.pred_reader.get_R_aslip(site, cmpt)
        plt.plot_date(shift_t(ts), regularize_y(ys), ls=ls, marker=marker, lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_cumu_disp(self, site, cmpt, loc=2, leg_fs=7,
                       if_ylim=False,
                       if_plot_added = False,
                       ):        
        self.plot_cumu_obs_linres(site, cmpt)
        y = self.plot_cumu_disp_pred(site, cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style='-^', label='Rco', color='orange')
        y += self.plot_E_cumu_slip(site, cmpt, color='green')
        y += self.plot_R_aslip(site, cmpt, color='black')
        
        plt.grid('on')
        if if_ylim:
            plt.ylim(calculate_lim(y))

        if if_plot_added:
            self.plot_cumu_disp_pred_added(site, cmpt)
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.gcf().autofmt_xdate()
        plt.title('Cumulative Disp.: {site} - {cmpt}'.format(
            site = get_true_name_by_id(site),
            cmpt = cmpt
            ))

    def plot_post_disp(self, site, cmpt, loc=2, leg_fs=7,
                       if_plot_added = False,
                       ):
        y = self.plot_post_obs_linres(site,cmpt, label='obs.')
        y += self.plot_post_disp_pred(site,cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style = '-^', label='Rco', color='orange')
        y += self.plot_E_aslip(site, cmpt, color='green')
        y += self.plot_R_aslip(site, cmpt, color='black')

        plt.grid('on')

        if if_plot_added:
            self.plot_post_disp_pred_added(site, cmpt)
            
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.gcf().autofmt_xdate()
        plt.title('Postseismic Disp. : {site} - {cmpt}'.format(
            site = get_true_name_by_id(site),
            cmpt = cmpt
            ))


    
 
