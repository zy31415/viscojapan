import numpy as np

x=np.arange(12).reshape([4,3])

idx = np.asarray([True, False, True])
idx2 = np.asarray([True, False, True])

print(x[idx,idx2])
