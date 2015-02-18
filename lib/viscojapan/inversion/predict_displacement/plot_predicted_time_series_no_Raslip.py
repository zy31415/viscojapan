from pylab import plt


from .deformation_partition_file_reader import DeformPartitionResultReader
from ...tsana.observation_database import ObservationDatatbaseReader
from ...sites_db import get_site_true_name
from ..result_file import ResultFileReader
from .plot_predicted_time_series import PredictedTimeSeriesPlotter

__all__ = ['PredictedTimeSeriesPlotterNoRaslip']


class PredictedTimeSeriesPlotterNoRaslip(PredictedTimeSeriesPlotter):
    def __init__(self,
                 partition_file,
                 result_file,
                 ):
        self.partition_file = partition_file
        reader = DeformPartitionResultReader(self.partition_file)
        self.Rco = reader.Rco
        self.Ecumu = reader.Ecumu
        self.d_added = reader.d_added

        self.result_file = result_file
        reader = ResultFileReader(self.result_file)
        self.d_pred = reader.get_pred_disp()

        self.plt = plt

        self.obs_db = '/home/zy/workspace/viscojapan/tsana/db/~observation.db'
        self.obs_reader = ObservationDatatbaseReader(self.obs_db)
        
    def plot_R_aslip(self, site, cmpt,
                     ls='-', marker='o',
                     lw=1, ms=2, label='Raslip',**kwargs):
        raise ValueError("No Raslip")

    def plot_cumu_disp(self, site, cmpt, loc=2, leg_fs=7,
                       if_ylim=False,
                       added_label = None,
                       ):        
        self.plot_cumu_obs_linres(site, cmpt)
        y = self.plot_cumu_disp_pred(site, cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style='-^', label='Rco', color='orange')
        y += self.plot_E_cumu_slip(site, cmpt, color='green')

        plt.grid('on')
        if if_ylim:
            plt.ylim(calculate_lim(y))

        self.plot_cumu_disp_pred_added(site, cmpt, label=added_label)
        plt.ylabel(r'm')
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.gcf().autofmt_xdate()
        plt.title('Cumulative Disp.: {site} - {cmpt}'.format(
            site = get_site_true_name(site_id=site),
            cmpt = cmpt
            ))

    def plot_post_disp(self, site, cmpt, loc=2, leg_fs=7,
                       added_label = None,
                       marker_for_obs = 'x',
                       ):
        y = self.plot_post_obs_linres(site,cmpt, label='obs.', marker=marker_for_obs)
        y += self.plot_post_disp_pred(site,cmpt, label='pred.')
        y += self.plot_R_co(site, cmpt,
                            style = '-^', label='Rco', color='orange')
        y += self.plot_E_aslip(site, cmpt, color='green')

        plt.grid('on')

        self.plot_post_disp_pred_added(site, cmpt, label=added_label)
        
        plt.legend(loc=loc, prop={'size':leg_fs})
        plt.ylabel(r'm')
        plt.gcf().autofmt_xdate()
        plt.title('Postseismic Disp. : {site} - {cmpt}'.format(
            site = get_site_true_name(site_id = site),
            cmpt = cmpt
            ))


    
