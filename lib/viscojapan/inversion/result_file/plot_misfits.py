import os
import tempfile
import shutil

import numpy as np

import latex

from .disp_result_reader import DispResultReader
from ...gmt.applications.plot_Z_at_sites import ZPlotter

__all__ = ['MisfitPlotter']

class MisfitPlotter(object):
    ''' Plot misfits of three components in a map view.
Combine each subplots using latex into a pdf file.
'''
    def __init__(self,
                 result_file
                 ):
        self.result_file = result_file
        self.analyser = DispResultReader(self.result_file)
        self.sites = self.analyser.sites

        self._cwd = tempfile.mkdtemp()

        self._subfig_wid = 0.49
        self._subfig_trim = 50,50,60,370
        
    def plot(self, output_file):
        doc = latex.LatexDoc()

        doc.elements = [
            self._plot_rms_co(),
            self._plot_rms_co_relative_to_coseismic_offset(),
            
            self._plot_rms_cumu(),
            self._plot_rms_cumu_relative_to_coseismic_offset(),

            self._plot_rms_post(),
            self._plot_rms_post_relative_to_coseismic_offset(),
            self._plot_rms_post_relative_to_max_postseismic_offset(),

            self._plot_rms_post_at_epoch(10),
            self._plot_rms_post_at_epoch(-1),
            ]

        cmpl = latex.PDFComplie(doc)
        cmpl.compile(output_file)

        self._clean()

    def _plot(self, es, ns, us, alls, caption,
              clim = [-3,-.5]):
        ana = self.analyser
        rms = {'e':es, 'n':ns, 'u':us, 'all':alls}
        
        fig = latex.Figure(caption = caption)

        for cmpt in 'e','n','u','all':
            fid, fn = tempfile.mkstemp(suffix='.pdf', dir=self._cwd)
            
            plt = ZPlotter(sites=self.sites, Z=rms[cmpt])
            plt.plot(clim=clim)
            plt.save(fn)

            subf = latex.Subfigure(
                width = self._subfig_wid,
                trim = self._subfig_trim,
                file = fn,
                caption='Component: %s'%cmpt,
                )
            fig.append_subfigure(subf)
        return fig

    def _plot_rms_cumu(self):
        ana = self.analyser
        es = ana.get_cumu_rms(subset_cmpt = [0],
                                 axis = 0)
        ns = ana.get_cumu_rms(subset_cmpt = [1],
                                 axis = 0)
        us = ana.get_cumu_rms(subset_cmpt = [2],
                                 axis = 0)
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)
        
        return self._plot(es, ns, us, alls, 'RMS of cumulative time series (m) at each station')

    def _plot_rms_post(self):
        ana = self.analyser
        es = ana.get_post_rms(subset_cmpt = [0],
                                 axis = 0)
        ns = ana.get_post_rms(subset_cmpt = [1],
                                 axis = 0)
        us = ana.get_post_rms(subset_cmpt = [2],
                                 axis = 0)
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)
        
        return self._plot(es, ns, us, alls, 'RMS of postseismic time series (m) at each station')

    def _plot_rms_co(self):
        ana = self.analyser
        
        es = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [0],
            axis = 0)
        ns = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [1],
            axis = 0)
        us = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [2],
            axis = 0)
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)
        
        return self._plot(es, ns, us, alls, 'RMS of coseismic offsets (m) at each station')

    def _plot_rms_co_relative_to_coseismic_offset(self):
        ana = self.analyser

        es = ana.get_cumu_rms(subset_epochs = [0], subset_cmpt = [0], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,0]
        es /= np.abs(co)
        
        ns = ana.get_cumu_rms(subset_epochs = [0], subset_cmpt = [1], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,1]
        ns /= np.abs(co)
        
        us = ana.get_cumu_rms(subset_epochs = [0], subset_cmpt = [2], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,2]
        us /= np.abs(co)
        
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)

        return self._plot(es, ns, us, alls,
                          'RMS of coseismic offsets at each station relative to predicted coseismic offsets.',
                          clim=[-2.3,1.4])

    def _plot_rms_cumu_relative_to_coseismic_offset(self):
        ana = self.analyser
        
        es = ana.get_cumu_rms(subset_cmpt = [0], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,0]
        es /= np.abs(co)
        
        ns = ana.get_cumu_rms(subset_cmpt = [1], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,1]
        ns /= np.abs(co)
        
        us = ana.get_cumu_rms(subset_cmpt = [2], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,2]
        us /= np.abs(co)
        
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)

        return self._plot(es, ns, us, alls,
                          'RMS of cumulative time series at each station relative to coseismic offsets.',
                          clim=[-2.3,1.4])

    def _plot_rms_post_relative_to_coseismic_offset(self):
        ana = self.analyser
        
        es = ana.get_post_rms(subset_cmpt = [0], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,0]
        es /= np.abs(co)
        
        ns = ana.get_post_rms(subset_cmpt = [1], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,1]
        ns /= np.abs(co)
        
        us = ana.get_post_rms(subset_cmpt = [2], axis = 0).flatten()
        co = ana.get_cumu_pred_3d()[0,:,2]
        us /= np.abs(co)
        
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)

        return self._plot(es, ns, us, alls,
                          'RMS of postseismic time series at each station relative to coseismic offsets.',
                          clim=[-2.2,1.6])

    def _plot_rms_post_relative_to_max_postseismic_offset(self):
        ana = self.analyser
        
        es = ana.get_post_rms(subset_cmpt = [0], axis = 0).flatten()
        co = ana.get_post_pred_3d()[-1,:,0]
        es /= np.abs(co)
        
        ns = ana.get_post_rms(subset_cmpt = [1], axis = 0).flatten()
        co = ana.get_post_pred_3d()[-1,:,0]
        ns /= np.abs(co)
        
        us = ana.get_post_rms(subset_cmpt = [2], axis = 0).flatten()
        co = ana.get_post_pred_3d()[-1,:,0]
        us /= np.abs(co)
        
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)

        return self._plot(es, ns, us, alls,
                          'RMS of postseismic time series at each station relative to postseismic offsets.',
                          clim=[-2.5,1])

    def _plot_rms_post_at_epoch(self, nth):
        ana = self.analyser
        es = ana.get_post_rms(subset_epochs = [nth], subset_cmpt = [0], axis = 0)
        ns = ana.get_post_rms(subset_epochs = [nth], subset_cmpt = [1], axis = 0)
        us = ana.get_post_rms(subset_epochs = [nth], subset_cmpt = [2], axis = 0)
        alls = np.sqrt((es**2 + ns**2 + us**2)/3.)
        
        return self._plot(es, ns, us, alls, 'RMS of postseismic offsets (m) at epoch %d at each station'%\
                          (self.analyser.epochs[nth]))
        
    def _clean(self):
        shutil.rmtree(self._cwd)
        
            
        

        
