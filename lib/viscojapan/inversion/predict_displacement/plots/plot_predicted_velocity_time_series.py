from pylab import plt
import numpy as np

from viscojapan.inversion.predict_displacement.deformation_partition_file_reader import DeformPartitionResultReader
from viscojapan.sites_db import get_site_true_name


from date_conversion import adjust_mjd_for_plot_date

__all__ = ['PredictedVelocityTimeSeriesPlotter']

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

class PredictedVelocityTimeSeriesPlotter(object):
    def __init__(self, partition_file):

        self.partition_file = partition_file
        reader = DeformPartitionResultReader(self.partition_file)
        self.Rco = reader.Rco
        self.Ecumu = reader.Ecumu
        self.Raslip = reader.Raslip
        self.d_added = reader.d_added

        self.plt = plt


    def plot_pred_vel_added(self, site, cmpt, color='red', lw=2, label=None, **kwargs):
        ys = self.d_added.vel_ts(site, cmpt) * 1000 * 365
        ts = self.d_added.get_epochs()[1:]
        plt.plot_date(shift_t(ts), regularize_y(ys), '-o', lw=lw, ms=2*lw,
                      color=color, label=label,
                      **kwargs)
        return list(ys)


    def plot_vel_R_co(self, site, cmpt,
                  style = '-^', lw=1, **kwargs):
        ys = self.Rco.vel_ts(site, cmpt) * 1000 * 365
        ts = self.Rco.get_epochs()[1:]

        plt.plot_date(shift_t(ts), regularize_y(ys), style, lw=lw, ms = 4*lw, **kwargs)
        return list(ys)

    def plot_vel_E_cumu_slip(self, site, cmpt,
                         lw=1, ms = 7,
                         label='E',**kwargs):
        ys = self.Ecumu.vel_ts(site, cmpt) * 1000 * 365
        ts = self.Ecumu.get_epochs()[1:]
        plt.plot_date(shift_t(ts), regularize_y(ys), '-+', lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_vel_R_aslip(self, site, cmpt,
                     ls='-', marker='o',
                     lw=1, ms=2, label='Raslip',**kwargs):
        ys = self.Raslip.vel_ts(site, cmpt) * 1000 * 365
        ts = self.Raslip.get_epochs()[1:]
        plt.plot_date(shift_t(ts), regularize_y(ys), ls=ls, marker=marker, lw=lw, ms=ms,
                 label = label,
                 **kwargs)
        return list(ys)

    def plot_vel_decomposition(self, site, cmpt, loc=0, leg_fs=7,
                       if_ylim=False
                       ):
        y = self.plot_pred_vel_added(site, cmpt, label='total')
        y += self.plot_vel_R_co(site, cmpt,
                            style='-^', label='Rco', color='orange')
        y += self.plot_vel_E_cumu_slip(site, cmpt, color='green')
        y += self.plot_vel_R_aslip(site, cmpt, color='black')
        
        plt.grid('on')
        if if_ylim:
            plt.ylim(calculate_lim(y))

        plt.ylabel(r'mm/yr')
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.gcf().autofmt_xdate()
        plt.title('Cumulative Disp.: {site} - {cmpt}'.format(
            site = get_site_true_name(site_id=site),
            cmpt = cmpt
            ))


 
