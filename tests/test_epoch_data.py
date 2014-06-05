import sys
from os.path import exists
import os

from numpy import ones

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.epochal_data import EpochalData

epoch_file1 = 'test1.h5'

if exists(epoch_file1):
    os.remove(epoch_file1)

# test writing:
    
epochs = range(1, 10)

ep = EpochalData(epoch_file1)

# test ep.set_epoch_value()
for epoch in epochs:
    ep.set_epoch_value(epoch, epoch*ones((10,1)))

# test ep.get_epoch_value()

ep.get_epoch_value(1)

ep.set_info('sites',[b'a',b'b',b'c',b'd',b'e',
                                          b'f',b'g',b'h',b'i'],
                     unit = 'meter')

### test reading:
### test ep.get_epochs()
epochs = ep.get_epochs()
print(epochs)

### test ep.get_epoch_value()
for epoch in range(1,10):
    val = ep.get_epoch_value(epoch)
    print(val)
##
### test interpolation
for epoch in range(1,9):
    val = ep.get_epoch_value(epoch+0.1) 
    print(val)

sites = ep.get_info('sites')
print(sites)
##
print(ep.has_info('sites'))
print(ep.has_info('xxxx'))
##
for epoch, val in ep.iter_epoch_values():
    print(epoch, val)
##
epoch_file2 = 'test2.h5'
if exists(epoch_file2):
    os.remove(epoch_file2)

ep2 = EpochalData(epoch_file2)
ep2.copy_info_from(epoch_file1)

ep.copy_info_to('test3.h5')
