from os.path import exists

def _assert_file_exists(fn):
    assert exists(fn), "File %s doesn't exist."%fn

# iterate text file
def if_line_is_commenting(ln):
    tp = ln.strip()
    if len(tp)==0:
        return True
    if tp[0] == '#':
        return True
    return False

def next_non_commenting_line(fid):
    for ln in fid:
        if not if_line_is_commenting(ln):
            yield ln
