from pylab import plt

from .pred_disp_database import PredDispToDatabaseReader

__all__ = ['TimeSeriesPlotter']

class TimeSeriesPlotter(object):
    def __init__(self,
                 pred_db,
                 ):
        self.pred_db = pred_db
        self.plt = plt

        self.obs_db = '/home/zy/workspace/viscojapan/tsana/db/~observation.db'

    def plot_linres(self, site, cmpt):
        reader = PredDispToDatabaseReader(self.pred_db)
        ts, ys = reader.get_time_series(site, cmpt)
        plt.plot(ts, ys)
        

    def plot_pred(self, site, cmpt):
        pass
    
