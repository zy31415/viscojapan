from pylab import plt

from .earth_model_file_reader import EarthModelFileReader

__all__ = ['plot_earth_model_file_along_depth_change']

def plot_earth_model_file_along_depth_change(
    earth_model_file,
    file_name_prefix = 'earth_model',
    file_type = 'pdf',
    if_show = False,)

    em = EarthModelFileReader('earth.modelBURG-SUM_40km')
    
    den = em.density
    _plot_base(den,[300,0],[2.5, 3.6],
          r'density ($g/cm^3$)')
    plt.savefig('%s_density.%s'%(file_name_prefix, file_type))
    if if_show:
        plt.show()
    plt.close()
    

    shear = em.shear/10**9
    _plot_base(shear,[300,0],[15, 110],
          r'shear modulus ($GPa$)')
    plt.savefig('%s_shear.%s'%(file_name_prefix, file_type))
    if if_show:
        plt.show()
    plt.close()

    bulk = em.bulk/10**9
    _plot_base(bulk,[300,0],[40, 200],
          r'bulk modulus ($GPa$)')
    plt.savefig('%s_bulk.%s'%(file_name_prefix, file_type))
    if if_show:
        plt.show()
    plt.close()

def _plot_base(dep, val, deplim_small, xlim_small, xlabel):
    plt.subplot(1,2,1)
    plt.plot(val, dep)
    plt.gca().invert_yaxis()
    plt.grid('on')
    plt.ylabel('depth/km')
    plt.xlabel(xlabel)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=-45)

    plt.subplot(1,2,2)
    plt.plot(val, dep)
    plt.gca().invert_yaxis()
    plt.grid('on')
    plt.ylim(deplim_small)
    plt.xlim(xlim_small)
    plt.xlabel(xlabel)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=-45)
