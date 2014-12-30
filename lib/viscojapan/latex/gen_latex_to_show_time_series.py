import shutil
from os.path import join, basename, splitext, exists

import pGMT
import latex
from ..gmt import plot_stations, plot_focal_mechanism_JMA

__all__ = ['LatexTimeSeriesShow']

class LatexTimeSeriesShow(object):
    def __init__(self,
                 site_groups,
                 captions,
                 labels,
                 ):
        self.site_groups = site_groups

        self.sites = []
        for sites in self.site_groups:
            self.sites += sites
            
        self.captions = captions
        self.labels = labels
        
        self.file_sites_map = 'figs/time_series_stations.pdf'

        self.dir_from = '/home/zy/workspace/viscojapan/inversions/inversion10/iter2/run3/analysis/time_series/plots/'
        self.dir_to = 'figs/time_series/'

    def fetch_plots(self):
        for site in self.sites:
            for cmpt in 'e','n','u':
                file_from = self._form_file_name_from(site=site, cmpt=cmpt)
                if not exists(file_from):
                    raise ValueError("File %s doesn't exit"%file_from)                  
                file_to = self._form_file_name_to(site, cmpt)            
                shutil.copyfile(file_from, file_to)
                
    def _form_file_name_from(self, site, cmpt):
        return join(self.dir_from,
                    '{site}.{cmpt}.post.pdf'.\
                    format(site=site, cmpt=cmpt))

    def _form_file_name_to(self, site, cmpt):
        return join(self.dir_to,
                    '{site}-{cmpt}-post.pdf'.\
                    format(site=site, cmpt=cmpt))

    def save_latex(self, fn):
        self.fetch_plots()
        self.plot_stations_map() 

        lt = latex.Latex()
        
        fig = self._gen_latex_for_sites_map()
        lt.elements.append(fig)

        for sites, cap, label in zip(self.site_groups, self.captions, self.labels):
            fig = self._gen_latex_onshore_time_series(sites, cap, label)
            lt.elements.append(fig)

        with open(fn, 'wt') as fid:
            lt.print(fid)

    def _gen_latex_for_sites_map(self):
        fig = latex.Figure(
            caption = '''Sites map.''',
            label = 'fig:sites_map_onshore_time_series'
            )
        width = 1.
        _file = '\\figsPath time_series_stations.pdf'
        subf = latex.Subfigure(
            width = width,
            trim = (50,50,50,200),
            file = _file,
            )
        fig.append_subfigure(subf)
        return fig

    def plot_stations_map(self):    
        gmt = pGMT.GMT()

        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = gmt.gplt

        gplt.psbasemap(
            R = '125/146/30/46',       # region
            JB = '135.5/38.5/35/41.5/16c', # projection
            B = '5', U='18/25/0',
            P='',K='',
            )

        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,150,-.',
            W = 'faint,dimgray',A='500',L='144/32/38/200+lkm+jt',
            O = '', K='')

        plot_stations(
            gplt, self.sites,
            S = 's.2',
            color = 'red',
            fill_color = 'red',
            fontcolor = 'blue',
            fontsize = '8',
            text_offset_X = 0,
            text_offset_Y = 0,
            )

        plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

        gplt.finish()
        gmt.save(self.file_sites_map)

    def _gen_latex_onshore_time_series(self, sites, caption, label):
        fig = latex.Figure(
            caption = caption,
            label = label,
            )

        width = 0.32

        for site in sites:
            for cmpt in 'e', 'n', 'u':
                _file = self._form_file_name_to(site, cmpt)
                _file = '\\figsPath time_series/%s'%(basename(_file))
                subf = latex.Subfigure(
                    width = width,
                    trim = (40,40,40,20),
                    file = _file,
                    )

                fig.append_subfigure(subf)
        return fig

        

    
