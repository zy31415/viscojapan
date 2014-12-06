from os.path import join
from ...utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

file_kur_top = join(this_script_dir,'kur_top.in')

file_kur_contours = join(this_script_dir,
                         'kur_contours.in')

file_plate_boundary = join(this_script_dir,
                           'PB2002_boundaries.gmt')

file_etopo1 = join(this_script_dir,
                   'ETOPO1_Bed_g_gmt4.grd')

topo_cpts = {
    'afrikakarte' : join(this_script_dir, 'afrikakarte.cpt'),
    'wiki-france' : join(this_script_dir, 'wiki-france.cpt'),
    'etopo1' : join(this_script_dir, 'ETOPO1.cpt'),
    'seminf-haxby' : join(this_script_dir, 'seminf-haxby.cpt'),
    }


__all__=['file_kur_top', 'file_kur_contours',
         'file_plate_boundary', 'file_etopo1','topo_cpts']
