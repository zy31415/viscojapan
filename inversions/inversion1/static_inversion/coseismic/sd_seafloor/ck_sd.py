import numpy as np

sds = np.logspace(-4, -1, 10)

for nsd, sd in enumerate(sds):
    print(nsd, sd)
