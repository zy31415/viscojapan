import numpy as np
epochs = [int(ii) for ii in np.linspace(0,1344,21)]

add_epochs = []

n=0
while epochs[n]<450:
    epoch = (epochs[n] + epochs[n+1])//2
    add_epochs.append(epoch)
    n += 1

epochs += add_epochs

epochs = sorted(epochs)
