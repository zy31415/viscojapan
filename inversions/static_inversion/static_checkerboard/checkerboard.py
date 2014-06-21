from numpy import asarray, dot
from numpy.linalg import norm

from checkerboard_static import CheckerBoardStatic

from alphas import alphas

chb = CheckerBoardStatic()
chb.set_up()

residual_norms = []
roughnesses = []

for alpha in alphas:
    sol = chb(alpha)
    m_inverted = asarray(sol['x'])

    roughness = dot(dot(m_inverted.T,
                        chb.lst.regularization_matrix.todense())
                    ,m_inverted)
    roughness = roughness[0,0]
    roughnesses.append(roughness)

    d_predicted = dot(chb.G, m_inverted)

    del_d = chb.d - d_predicted
    residual_norm = norm(del_d)
    residual_norms.append(residual_norm)
    
import pickle
with open('L-curve.pkl','wb') as fid:
    pickle.dump((residual_norms, roughnesses),fid)

