import viscojapan as vj

from epochs import epochs

slip = vj.inv.ep.EpochSlip('../../slip/extra_slip_EXP.h5')

file_G0 = '../../../green_function_large_scale/G_large_scale.h5'

pred = vj.inv.DeformPartitionerNoDifferentiation(
    file_G0,
    epochs,
    slip
    )
    
pred.save('deformation_partition_large_scale.h5')


