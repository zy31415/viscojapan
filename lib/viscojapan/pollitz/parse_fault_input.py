import glob
from ..utils import next_non_commenting_line

def _parse_first_line(ln):
    tp = ln.split()
    res = {}
    res['bottom'] = float(tp[0])
    res['top'] = float(tp[1])
    res['dip'] = float(tp[2])
    return res

def _parse_subflts_section(fid):
    ln = fid.readline()
    num_subflts = int(ln)
    res = {}
    res['num_subflts'] = num_subflts
    
    lons = []
    lats = []
    lens = []
    strikes = []
    rakes = []
    slips = []

    for nth, ln in enumerate(next_non_commenting_line(fid)):
        tp = ln.strip().split()
        assert len(tp)==6,'Record is wrong.'
        lats.append(float(tp[0]))
        lons.append(float(tp[1]))
        
        lens.append(float(tp[2]))
        strikes.append(float(tp[3]))
        rakes.append(float(tp[4]))
        slips.append(float(tp[5]))
    assert nth+1 == num_subflts, "#subflts is wrong."
    res['lons'] = lons
    res['lats'] = lats
    res['lens'] = lens
    res['strikes'] = strikes
    res['rakes'] = rakes
    res['slips'] = slips

    return res

def parse_fault_input(fn):
    with open(fn,'rt') as fid:
        ln = fid.readline()
        res1 = _parse_first_line(ln)
        res2 = _parse_subflts_section(fid)
        res1.update(res2)
    return res1

        
    
