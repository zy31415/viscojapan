import numpy as np
epochs = [int(ii) for ii in np.linspace(0,1100,21)]

add_epochs = []
for n in range(7):
    epoch = (epochs[n] + epochs[n+1])//2
    add_epochs.append(epoch)

epochs += add_epochs

epochs = sorted(epochs)
