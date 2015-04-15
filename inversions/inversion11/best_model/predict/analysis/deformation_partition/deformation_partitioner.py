import viscojapan as vj

from epochs import epochs

reader = vj.inv.ResultFileReader('../../nrough_06_naslip_11.h5')
slip = reader.get_slip()

file_G0 = '../../../green_function/G.h5'

part = vj.inv.DeformPartitionerNoDifferentiation(
    file_G0,
    epochs,
    slip
    )
    
part.save('deformation_partition.h5')
