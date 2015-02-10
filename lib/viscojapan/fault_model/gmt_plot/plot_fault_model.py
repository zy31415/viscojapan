import tempfile

import numpy as np

__author__ = 'zy'
__all__ = ['gplt_fault_meshes','gplt_fault_meshes_marking_dip_changes', 'gplt_marking_dip_change_on_fault_meshes']

def gplt_fault_meshes(gplt, fault, W='thick,red'):
    reader = fault
    lats = reader.LLats
    lons = reader.LLons
    with tempfile.NamedTemporaryFile('w+t') as fid:
        _plot_fault_model_write_multisegment_file(lons, lats, fid)
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            R = '', J = '', O='' ,K='' ,W=W)

def gplt_fault_meshes_marking_dip_changes(gplt, fault):
    gplt_fault_meshes(gplt, fault, W = 'thin,red,-')
    gplt_marking_dip_change_on_fault_meshes(gplt, fault)

def _plot_fault_model_write_multisegment_file(lons, lats, fid):
    for lon, lat in zip(lons, lats):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))
    for lon, lat in zip(lons.T, lats.T):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))

def gplt_marking_dip_change_on_fault_meshes(
        gplt, fault,
        width='thickest',
        color='red'):
    llats = fault.LLats
    llons = fault.LLons
    ddips = fault.ddips

    dips = ddips[:,0]

    nodes = _get_value_changing_nodes(dips)
    nodes1 = nodes
    nodes2 = nodes[1:] + [len(dips)-1]

    for n1, n2 in zip(nodes1, nodes2):
        box = _get_a_drawing_box(n1, n2, llons, llats)
        _gplt_box(gplt, box, W='{width},{color}'.format(width=width, color=color))


def _get_value_changing_nodes(arr):
    _dip = arr[0]
    nodes = [0]
    for nth, d in enumerate(arr[1:]):
        if d != _dip:
            nodes.append(nth+1)
            _dip = d
    return nodes

def _get_a_drawing_box(n1,n2, llons, llats):
    p1 = llons[n1,0], llats[n1,0]
    p2 = llons[n1,-1], llats[n1,-1]
    p3 = llons[n2,-1], llats[n2,-1]
    p4 = llons[n2,0], llats[n2,0]
    return p1, p2, p3, p4

def _gplt_box(gplt, box, W='thickest,red'):
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for p in box:
            fid.write('%f %f\n'%(p[0], p[1]))
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            R = '', J = '', O='' ,K='' ,W=W, L='')
