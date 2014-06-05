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

# test EpochalData.set_epoch_value()
for epoch in epochs:
    EpochalData.set_epoch_value(epoch_file1,epoch, epoch*ones((10,1)))

# test EpochalData.get_epoch_value()

EpochalData.get_epoch_value(epoch_file1,1)

EpochalData.set_info(epoch_file1,'sites',[b'a',b'b',b'c',b'd',b'e',
                                          b'f',b'g',b'h',b'i'],
                     unit = 'meter')

# test reading:
# test EpochalData.get_epochs()
epochs = EpochalData.get_epochs(epoch_file1)
print(epochs)

# test EpochalData.get_epoch_value()
for epoch in range(1,10):
    val = EpochalData.get_epoch_value(epoch_file1,1)
    print(val)

# test interpolation
for epoch in range(1,9):
    val = EpochalData.get_epoch_value(epoch_file1,epoch+0.1) 
    print(val)

sites = EpochalData.get_info(epoch_file1, 'sites')
print(sites)

print(EpochalData.has_info(epoch_file1,'sites'))
print(EpochalData.has_info(epoch_file1,'xxxx'))

for epoch, val in EpochalData.iter_epoch_values(epoch_file1):
    print(epoch, val)

epoch_file2 = 'test2.h5'
if exists(epoch_file2):
    os.remove(epoch_file2)
    
EpochalData.copy_info(epoch_file1, epoch_file2)
