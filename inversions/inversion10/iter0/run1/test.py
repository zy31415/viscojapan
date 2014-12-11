import numpy as np

x = np.arange(0,1,.1)
y = np.arange(0,10,1)

xx, yy = np.meshgrid(x,y)

tp = np.indices((10,10))

def pop_from_center(center, arr1, arr2):
    assert len(center) ==2
    idx = []
    for ith in range(len(arr1)):
        for jth in range(len(arr2)):
            idx.append((ith, jth))
    idx_sorted = sorted(idx, key=lambda x : np.sqrt((x[0]-center[0])**2+(x[1]-center[1])**2))

    idx1_sorted = [ii[0] for ii in idx_sorted]
    idx2_sorted = [ii[1] for ii in idx_sorted]

    arr1_sorted = arr1[idx1_sorted]
    arr2_sorted = arr2[idx2_sorted]

    for idx1, idx2 in zip(idx1_sorted, idx2_sorted):
        yield(idx1, idx2, arr1[idx1], arr2[idx2])
            

for ii in pop_from_center((4,6), x, y):
    print(ii)
