import viscojapan as vj
from pylab import plt

site = 'G002'

def get_prediction(file_pred, site, cmpt):
    reader = vj.inv.DeformPartitionResultReader(
        fn = file_pred)
    disp = reader.d_added
    y = disp.cumu_ts(site, cmpt)
    t = disp.get_epochs()
    return y, t


for cmpt in 'enu':
    y1, t1 = get_prediction('./deformation_partition/deformation_partition.h5',
                            site, cmpt)
    y2, t2 = get_prediction('../../../iter1/run0/analysis/deformation_partition/deformation_partition.h5',
                            site, cmpt)    
    plt.plot(t1, y1,'x-',label = 'with inferred model')
    plt.plot(t2, y2,'>-',label = 'with diff. model')
    plt.title('%s - %s'%(site, cmpt))
    plt.legend(loc=0)
    plt.savefig('%s-%s.png'%(site, cmpt))
    #plt.show()
    plt.close()
