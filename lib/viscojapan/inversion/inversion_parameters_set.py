class InversionParametersSet(object):
    ''' Inversion parameters include the following parameters
in the following formula:
||W G B m - W d|| - ||L (B m + B m0)||
(m is output)
'''
    def __init__(self,
                 G,
                 d,
                 L = None,
                 W = None,
                 B = None,
                 Bm0 = None
                 ):
        self.G = G
        self.d = d
        self.L = L
        self.W = W
        self.B = B
        self.Bm0 = Bm0

        self._check_input()
            
    def _check_input(self):
        ''' Assert the following operation is possible:
||W G B m - W d|| - ||L (B m + B m0)||
W - sparse, weighting matrix
G - ndarray, green's function
B - sparse, basis matrix
L - sparse, regularization matrix
'''
        self.num_obs = _assert_column_vector(self.d)

        if self.W is None:
            self.W = sparse.eye(num_obs)
        else:
            assert self.W.shape[1] == self.G.shape[0]

        self.num_pars = self.B.shape[1]

        if self.B is None:
            self.B = sparse.eye(num_pars)
        else:
            self.G.shape[1] == self.B.shape[0]

        num_subflts = self.B.shape[0]
        if self.L is None:
            self.L = sparse.csr_matrix((1,num_subflts),dtype=float)
        else:
            assert self.L.shape[1] == num_subflts

        if self.Bm0 is None:
            self.Bm0 = zeros([self.num_pars, 1])
        else:
            assert self.Bm0.shape == (self.num_pars, 1)

        # assert type:
        self.W = csr_matrix(self.W)
        self.B = csr_matrix(self.B)
        self.L = csr_matrix(self.L)
        assert isinstance(self.G, ndarray)
        assert isinstance(self.Bm0, ndarray)
