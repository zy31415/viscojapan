import warnings

from numpy import zeros

from viscojapan.fault_model import FaultFileReader
from ...utils import assert_nonnegative_integer

def gen_checkerboard_slip(num_subflts_dip, num_subflts_strike,
                           dip_patch_size=1,  strike_patch_size=1):
    N = num_subflts_strike
    M = num_subflts_dip
    dN = strike_patch_size
    dM = dip_patch_size

    assert_nonnegative_integer(N)
    assert_nonnegative_integer(M)
    assert_nonnegative_integer(dN)
    assert_nonnegative_integer(dM)

    res = zeros((M, N),'float')
    for mth in range(0, M, dM):
        val1 = (mth//dM)%2
        for nth in range(0, N, dN):
            val2 = ((nth//dN)+val1)%2
            res[mth:mth+dM, nth:nth+dN] = val2
            #print('row: %d:%d || col: %d:%d = %f'%(mth,mth+dM,nth,nth+dN,val2))
            
    return res

def gen_checkerboard_slip_from_fault_file(
    fault_file,
    dip_patch_size=1,
    strike_patch_size=1
    ):    
    fid = FaultFileReader(fault_file)
    num_subflts_dip = fid.num_subflt_along_dip
    num_subflts_strike = fid.num_subflt_along_strike
    return gen_checkerboard_slip(num_subflts_dip, num_subflts_strike,
                           dip_patch_size = dip_patch_size,
                           strike_patch_size = strike_patch_size)
    
def gen_checkerboard_slip2(num_subflts_strike, num_subflts_dip):
    warnings.warn("deprecated", DeprecationWarning)
    res = zeros((num_subflts_dip, num_subflts_strike),'float')
    for mth in range(num_subflts_strike):
        res[mth%2::2,mth] = 1.
    return res
