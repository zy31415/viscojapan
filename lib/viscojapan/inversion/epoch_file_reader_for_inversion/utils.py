import h5py

__author__ = 'zy'
__all__ = ['convert_old_G_format_to_new']

def convert_old_G_format_to_new(f_old, f_new):
    h1 = h5py.File(f_old,'r')

    sh = h1['epochs/0000'].shape

    h2 = h5py.File(f_new, 'w')

    h2.create_dataset(name = 'data3d',
                      shape = (28,sh[0],sh[1]),
                      dtype = 'double'
                      )
    epochs = range(0,1621,60)
    for nth, epoch in enumerate(epochs):
        h2['data3d'][nth,:,:] = h1['epochs/%04d'%epoch]

    h2.create_dataset(name='epochs',
                      dtype='int',
                      data=epochs)

    sites = h1['info/sites']
    h2.create_dataset(name='sites', dtype="S4", data=sites)

    for name in 'He', 'log10(He)','log10(visK)','log10(visM)',\
        'num_subflts','rake','visK','visM':
        h2.create_dataset(name=name,
                          data=h1['info/%s'%name])

    h1.close()
    h2.close()
