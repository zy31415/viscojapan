from viscojapan.epochal_data import EpochalG, EpochalDisplacement,\
     conv_stack, vstack_column_vec
from viscojapan.least_square import LeastSquare, TikhonovSecondOrder

G = EpochalG('/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5',
             'sites')
disp = EpochalDisplacement('simulated_disp.h5', 'sites')

epochs = [0, 500, 1100]

G_stacked = conv_stack(G, epochs)

d = vstack_column_vec(disp, epochs)

tik = TikhonovSecondOrder()
tik.nrows_slip = 10
tik.ncols_slip = 25
tik.row_norm_length = 1
tik.col_norm_length = 28./23.03
tik.num_epochs = len(epochs)
tik.num_nlin_pars = 0

lst = LeastSquare()
lst.G = G_stacked
lst.d = d
lst.alpha = 10
lst.regularization_matrix = tik()

solution = lst()
