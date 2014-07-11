class Regularization(object):
    def __call__(self, *args, **kwargs):
        return self.generate_regularization_matrix(*args, **kwargs)        

    def generate_regularization_matrix(self):
        raise NotImplementedError(
            "This interface returns the regularization matrix.")
