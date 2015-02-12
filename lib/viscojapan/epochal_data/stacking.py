from os.path import exists

from scipy.sparse import bmat
from numpy import vstack, zeros

from .epochal_data import EpochalData
from ..utils import assert_integer, assert_nonnegative_integer, \
     assert_col_vec_and_get_nrow

def conv_stack(epoch_data, epochs):
    ''' Stack epoch_data according to time indicated by epochs to
matrix that represents convolution.
'''
    N = len(epochs)

    sh1, sh2 = epoch_data.get_data_at_epoch(0).shape

    G=zeros((sh1*N, sh2*N), dtype='float')
    for nth in range(0, N):
        t1 = epochs[nth]
        for mth in range(nth, N):
            t2 = epochs[mth]
            #print(t2,t1,t2-t1)
            G_ = epoch_data.get_data_at_epoch(t2-t1)
            #print(mth*sh1,(mth+1)*sh1,nth*sh2,(nth+1)*sh2)
            G[mth*sh1:(mth+1)*sh1,
              nth*sh2:(nth+1)*sh2] = G_
    return G

def conv_stack_sparse(epoch_data, epochs):
    ''' Sparse stacking is slower.
See test routine.
'''
    N = len(epochs)
    G=[]
    for nth in range(N):
        G.append([None]*N)

    for nth in range(0, N):
        t1 = epochs[nth]
        for mth in range(nth, N):
            t2 = epochs[mth]
            #print(t2,t1,t2-t1)
            _G = epoch_data.get_data_at_epoch(t2-t1)
            G[mth][nth] = _G
    G_sparse = bmat(G)
    return G_sparse    

def vstack_column_vec(epoch_data, epochs):
    res = epoch_data.get_data_at_epoch(epochs[0])
    assert_col_vec_and_get_nrow(res)
    for epoch in epochs[1:]:
        res = vstack((res,epoch_data.get_data_at_epoch(epoch)))
    return res

def _assert_a_is_integer_multiple_of_b(a,b):
    assert_integer(a)
    assert_integer(b)
    assert a%b ==0 , 'a is not integer multiple of b.'
    return a//b

def _check_input_for_breaking_a_vec(vec, epochs, epoch_file,
                                  rows_per_epoch=None):
    # check input:
    num_rows = assert_col_vec_and_get_nrow(vec)
    num_epochs = len(epochs)

    _rows_per_epoch = _assert_a_is_integer_multiple_of_b(num_rows, num_epochs)
    if rows_per_epoch is not None:
        assert_nonnegative_integer(rows_per_epoch)
        assert _rows_per_epoch == rows_per_epoch, \
               'num_epochs and rows_per_epoch are inconsistant'
    else:
        rows_per_epoch = _rows_per_epoch
        
    assert not exists(epoch_file), "File %f exists already."%epoch_file

    return rows_per_epoch
    

def break_col_vec_into_epoch_file(vec, epochs, epoch_file,
                                  rows_per_epoch=None, info_dic={}):
    rows_per_epoch =\
        _check_input_for_breaking_a_vec(vec, epochs, epoch_file, rows_per_epoch)

    # Arguments checking done.
    ep = EpochalData(epoch_file)
    for nth, epoch in enumerate(epochs):
        val = vec[nth*rows_per_epoch : (nth+1)*rows_per_epoch, :]
        ep.set_epoch_value(epoch, val)
    
    ep.set_info_dic(info_dic)

def break_m_into_incr_slip_file(vec, epochs, epoch_file,
                                  rows_per_epoch=None, info_dic={}):
    break_col_vec_into_epoch_file(vec, epochs, epoch_file,
                                  rows_per_epoch, info_dic)

def break_m_into_slip_file(vec, epochs, epoch_file,
                                  rows_per_epoch=None, info_dic={}):
    rows_per_epoch =\
        _check_input_for_breaking_a_vec(vec, epochs, epoch_file, rows_per_epoch)
    
    # Arguments checking done.
    ep = EpochalData(epoch_file)
    for nth, epoch in enumerate(epochs):
        val = vec[0 : rows_per_epoch, :].copy()
        for mth in range(1, nth+1):
            val += vec[mth*rows_per_epoch : (mth+1)*rows_per_epoch, :]
        ep.set_epoch_value(epoch, val)
    
    ep.set_info_dic(info_dic)
               
        
    
    
