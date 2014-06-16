from os.path import exists

from scipy.sparse import bmat
from numpy import vstack, zeros

from .epochal_data import EpochalData

def conv_stack(epoch_data, epochs):
    ''' Stack epoch_data according to time indicated by epochs to
matrix that represents convolution.
'''
    N = len(epochs)

    sh1, sh2 = epoch_data.get_epoch_value(0).shape

    G=zeros((sh1*N, sh2*N), dtype='float')
    for nth in range(0, N):
        t1 = epochs[nth]
        for mth in range(nth, N):
            t2 = epochs[mth]
            #print(t2,t1,t2-t1)
            G_ = epoch_data.get_epoch_value(t2-t1)
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
            _G = epoch_data.get_epoch_value(t2-t1)
            G[mth][nth] = _G
    G_sparse = bmat(G)
    return G_sparse

def _assert_column_vector(res):
    sh = res.shape
    assert len(sh) ==2, "Wrong dimension. Must be column vector."
    assert sh[1] == 1, "Column number should 1."
    return sh[0]
    

def vstack_column_vec(epoch_data, epochs):
    res = epoch_data.get_epoch_value(epochs[0])
    _assert_column_vector(res)
    for epoch in epochs[1:]:
        res = vstack((res,epoch_data.get_epoch_value(epoch)))
    return res

def _assert_integer(var):
    assert isinstance(var, int), "%s is not an integer."%str(var)
    
def _assert_nonnegative_integer(var):
    _assert_integer(var)
    assert var >= 0, "%d is not non negative."%str(var)

def _assert_a_is_integer_multiple_of_b(a,b):
    _assert_integer(a)
    _assert_integer(b)
    assert a%b ==0 , 'a is not integer multiple of b.'
    return a//b
    
def break_col_vec_into_epoch_file(vec, epochs, epoch_file,
                                  rows_per_epoch=None, info_dic={}):
    # check input:
    num_rows = _assert_column_vector(vec)
    num_epochs = len(epochs)

    _rows_per_epoch = _assert_a_is_integer_multiple_of_b(num_rows, num_epochs)
    if rows_per_epoch is not None:
        _assert_nonnegative_integer(rows_per_epoch)
        assert _rows_per_epoch == rows_per_epoch, \
               'num_epochs and rows_per_epoch are inconsistant'
    else:
        rows_per_epoch = _rows_per_epoch
        
    assert not exists(epoch_file), "File %f exists already."%epoch_file

    # Arguments checking done.
    ep = EpochalData(epoch_file)
    for nth, epoch in enumerate(epochs):
        val = vec[nth*rows_per_epoch : (nth+1)*rows_per_epoch, :]
        ep.set_epoch_value(epoch, val)
    
    ep.set_info_dic(info_dic)
    

    
        
               
        
    
    
