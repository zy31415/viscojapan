from pylab import plt

__all__ = ['plot_earth_model_file_depth_change']

def plot_earth_model_file_depth_change(
    earth_model_file,
    output_fig_prefix,
    output_fig_type,
    if_show = False):
    
    den = em.density
    _plot(den,[300,0],[2.5, 3.6],
          r'density ($g/cm^3$)')
    plt.savefig('earth_model_density.pdf')
    plt.close()
    #plt.show()

    shear = em.shear/10**9
    _plot(shear,[300,0],[15, 110],
          r'shear modulus ($GPa$)')
    plt.savefig('earth_model_shear.pdf')
    plt.close()
    #plt.show()

    bulk = em.bulk/10**9
    _plot(bulk,[300,0],[40, 200],
          r'bulk modulus ($GPa$)')
    plt.savefig('earth_model_bulk.pdf')
    plt.show()

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
