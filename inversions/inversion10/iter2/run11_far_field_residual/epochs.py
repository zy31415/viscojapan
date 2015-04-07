import numpy as np

epochs_list = []

ts = np.arange(0,1344, 365/2)

for ti in ts[1:]:
    epochs = [int(ii) for ii in np.linspace(0,ti,31)]
    epochs_list.append(epochs)


