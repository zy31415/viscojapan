from numpy import vstack, zeros

def conv_stack(epoch_data, epochs, warning = False):
    ''' Stack epoch_data according to time indicated by epochs to
matrix that represents convolution.
'''
    if Warning:
        print("    Caution: Function conv_stack is running. Large memory required.")
        
    N = len(epochs)

    sh1, sh2 = epoch_data.get_epoch_value(0).shape

    G=zeros((sh1*N, sh2*N))
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

def _check_if_column_vector(epoch_data):
    sh = epoch_data.get_epoch_value(0).shape
    assert len(sh) ==2, "Wrong dimension. Must be column vector."
    assert sh[1] == 1, "Column number should 1."
    

def vstack_column_vec(epoch_data, epochs):
    _check_if_column_vector(epoch_data)
    res = epoch_data.get_epoch_value(epochs[0])
    for epoch in epochs[1:]:
        res = vstack((res,epoch_data.get_epoch_value(epoch)))
    return res
        
    
