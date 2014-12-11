import glob
from os.path import basename

import viscojapan as vj

G_olds = glob.glob('../../iter0/green_function/G*.h5')

for G_old in G_olds:
    print(G_old)
    G_new = basename(G_old)
    reader = vj.EpochalFileReader(G_old)
    epochs = reader.get_epochs()

    with vj.EpochalFileWriter(G_new) as writer:
        for epoch in epochs:
            tp = reader[epoch]
            writer[epoch] = tp[:,:336]
        writer.copy_info_from(G_old)
