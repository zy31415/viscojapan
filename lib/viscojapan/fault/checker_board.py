from numpy import zeros

def gen_checker_board_slip(num_subflts_strike, num_subflts_dip):
    res = zeros((num_subflts_dip, num_subflts_strike),'float')
    for mth in range(num_subflts_strike):
        res[mth%2::2,mth] = 1.
    return res
    
