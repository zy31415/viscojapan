from numpy import asarray, dot

from .epochal_data import EpochalData

class FormPredDisplacements(object):
    def __init__(self, inversion):
        self.inversion = inversion
        self.num_of_observation = 1300

    def _gen_predicated(self):
        m = asarray(self.inversion.solution['x'],float).flatten()
        G = self.inversion.least_square.G
        num_nlin_pars = len(self.inversion.formulate_occam.non_lin_par_vals)
        npars0 = asarray(self.inversion.formulate_occam.non_lin_par_vals,
                                   float)
        
        G1 = G[:,:-num_nlin_pars]
        G2 = G[:,-num_nlin_pars:]
        
        slip = m[:-num_nlin_pars]
        npars = m[-num_nlin_pars:]

        d = dot(G1,slip)

        delta_d = dot(G2, npars - npars0)

        d = d+delta_d

        d = d.reshape([-1,1])

        return d

    def gen_pred_displacements_file(self, file_name):
        self.d = self._gen_predicated()
        
        epochs = self.inversion.epochs

        obs = EpochalData(file_name)
        for nth, epoch in enumerate(epochs):
            obs.set_epoch_value(epoch, self.d[nth*self.num_of_observation:\
                                              (nth+1)*self.num_of_observation,0])
        

        
        

        
        
        
