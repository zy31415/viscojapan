import tempfile

__author__ = 'zy'
__all__ = ['gplt_fault_model']

def gplt_fault_model(gplt, fault):
    reader = fault
    lats = reader.LLats
    lons = reader.LLons
    with tempfile.NamedTemporaryFile('w+t') as fid:
        _plot_fault_model_write_multisegment_file(lons, lats, fid)
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            R = '', J = '', O='' ,K='' ,W='thick,red')

def _plot_fault_model_write_multisegment_file(lons, lats, fid):
    for lon, lat in zip(lons, lats):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))
    for lon, lat in zip(lons.T, lats.T):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))
