from pylab import plt

from .pred_disp_database import PredDispToDatabaseReader
from ...tsana.observation_database import ObservationDatatbaseReader

__all__ = ['TimeSeriesPlotter']

class TimeSeriesPlotter(object):
    def __init__(self,
                 pred_db,
                 ):
        self.pred_db = pred_db
        self.plt = plt

        self.obs_db = '/home/zy/workspace/viscojapan/tsana/db/~observation.db'

    def plot_cumu_disp_pred(self, site, cmpt, color='red', lw=2.5, **kwargs):
        reader = PredDispToDatabaseReader(self.pred_db)
        ts, ys = reader.get_cumu_disp_pred(site, cmpt)
        plt.plot(ts, ys, '-', lw=lw, color=color, **kwargs)
        

    def plot_linres(self, site, cmpt, **kwargs):
        reader = ObservationDatatbaseReader(self.obs_db)
        ts, ys = reader.get_time_series(site, cmpt)
        plt.plot(ts, ys, 'x', **kwargs)


    def plot_post_disp_pred(self, site, cmpt, **kwargs):
        reader = ObservationDatatbaseReader(self.obs_db)
        ts, ys = reader.get_post_disp_pred(site, cmpt)
        plt.plot(ts, ys, 'x', **kwargs)
    
