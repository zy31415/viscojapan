from numpy import loadtxt

from ...utils import next_non_commenting_line

def read_flt_file_for_stdin(fname, section):
    body = ''
    with open(fname,'rt') as fid:
        for nth, ln in enumerate(next_non_commenting_line(fid)):
            if nth == 0:
                head = ln
            else:
                body += (ln)

    if section == 'whole':
        return head + body

    if section =='head':
        return head

    if section == 'body':
        return body
    
    raise ValueError('Wrong parameter.')


def read_sites_file_for_stdin(fname):
    tp = loadtxt(fname,'4a, 2f')
    out = '%d\n'%(len(tp))
    for ii in tp:
        lon = ii[1][0]
        lat = ii[1][1]
        site = ii[0]
        out += '%f %f %s\n'%(lat, lon, site)
    return out
    
