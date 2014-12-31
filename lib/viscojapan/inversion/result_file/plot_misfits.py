import os

import numpy as np

import latex

from .disp_analyser import DispAnalyser
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
        self.analyser = DispAnalyser(self.result_file)
        self.sites = self.analyser.result_file_reader.sites

        self._cwd = tempfile.mkdtemp()
        
    def plot(self):
        self._compute_rms()

        for key, value in self.rms.items():
            print(key)
            plt = ZPlotter(sites=self.sites, Z=value)
            plt.plot(clim=[-3,-.5])
            plt.save('%s.pdf'%key)        

    def _compute_rms(self):
        ana = self.analyser
  
        rms_post_e = ana.get_post_rms(subset_cmpt = [0],
                                 axis = 0)
        rms_post_n = ana.get_post_rms(subset_cmpt = [1],
                                 axis = 0)
        rms_post_u = ana.get_post_rms(subset_cmpt = [2],
                                 axis = 0)
        rms_post = np.sqrt((rms_post_e**2 + rms_post_n**2 + rms_post_u**2)/3.)

        rms_co_e = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [0],
            axis = 0)
        rms_co_n = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [1],
            axis = 0)
        rms_co_u = ana.get_cumu_rms(
            subset_epochs = [0],
            subset_cmpt = [2],
            axis = 0)
        rms_co = np.sqrt((rms_co_e**2 + rms_co_n**2 + rms_co_u**2)/3.)


        rms={}
        rms['rms_cumu_e'] = rms_cumu_e
        rms['rms_cumu_n'] = rms_cumu_n
        rms['rms_cumu_u'] = rms_cumu_u
        rms['rms_cumu'] = rms_cumu
        rms['rms_post_e'] = rms_post_e
        rms['rms_post_n'] = rms_post_n
        rms['rms_post_u'] = rms_post_u
        rms['rms_post'] = rms_post
        rms['rms_co_e'] = rms_co_e
        rms['rms_co_n'] = rms_co_n
        rms['rms_co_u'] = rms_co_u
        rms['rms_co'] = rms_co
        self.rms = rms

    def _plot_rms_cumu(self):
        ana = self.analyser
        rms = {}
        rms['e'] = ana.get_cumu_rms(subset_cmpt = [0],
                                 axis = 0)
        rms['n'] = ana.get_cumu_rms(subset_cmpt = [1],
                                 axis = 0)
        rms['u'] = ana.get_cumu_rms(subset_cmpt = [2],
                                 axis = 0)
        rms['all'] = np.sqrt((rms_cumu_e**2 + rms_cumu_n**2 + rms_cumu_u**2)/3.)

        fig = latex.Figure(
            caption = 'RMS of cumulative time series')

        for key, value in self.rms.items():
            fn = tempfile.mkstemp(suffix='.pdf', dir=self._cwd)
            
            plt = ZPlotter(sites=self.sites, Z=value)
            plt.plot(clim=[-3,-.5])
            plt.save(fn)

            subf = latex.Subfigure(
                width = width,
                trim = trim,
                file = fn,
                caption='Component: %s'%cmpt,
                )
            fig.append_subfigure(subf)
        return fig



    def _compute_rms_relative_to_coseismic_offset(self):
        pass

    def combine(self, output_file):        
        trim = (20, 0, 10, 5)
        cmpts = 'e', 'n', 'u'
        kinds = 'co', 'cumu', 'post'
        captions = 'RMS of coseismic time series', \
                   'RMS of cumulative time series', \
                   'RMS of postseismic time series',\
                  
        width = 0.48

        doc = latex.LatexDoc()
        doc.elements = []

        trim = (50,50,60,370)
        for kind, cap in zip(kinds, captions):
            fig = latex.Figure(
                caption = cap)
            for cmpt in cmpts:
                subf = latex.Subfigure(
                    width = width,
                    trim = trim,
                    file = 'rms_%s_%s.pdf'%(kind, cmpt),
                    caption='Component: %s'%cmpt,
                    )
                fig.append_subfigure(subf)

            subf = latex.Subfigure(    
                width = width,
                trim = trim,
                file = 'rms_%s.pdf'%(kind),
                caption = 'All three components'
                )
            fig.append_subfigure(subf)

            doc.elements.append(fig)

        cmpl = latex.PDFComplie(doc)
        cmpl.compile(output_file)
        self._clean()
        
    def _clean(self):
        for key in self.rms.keys():
            os.remove('%s.pdf'%key)
            
        

        
