__doc__ = """This module defines errors in the process of regression."""
__all__ = ['Status',
           'IterFail','IterStop',
           'FailMatSing','FailBigChq','FailOverCorrection',
           'StopBigLam','StopSlowChisDrop','Stop2ManyIter']


class Status(Exception):
    pass

class IterFail(Status):
    pass

class IterStop(Status):
    pass
    

class FailMatSing(IterFail):
    def __init__(self):
        IterFail.__init__(self)
        self.message = 'Singular Matrix.'

class FailBigChq(IterFail):
    def __init__(self):
        IterFail.__init__(self)
        self.message = 'Larger chisq. Return back.'

class FailOverCorrection(IterFail):
    def __init__(self):
        IterFail.__init__(self)
        self.message = 'Over correction.'

class StopBigLam(IterStop):
    def __init__(self):
        IterStop.__init__(self)
        self.message = 'Large lambda. Stop.'

class StopSlowChisDrop(IterStop):
    def __init__(self):
        IterStop.__init__(self)
        self.message = 'Slow chisquare drop. Stop.'

class Stop2ManyIter(IterStop):
    def __init__(self):
        IterStop.__init__(self)
        self.message = 'Too many iterations. Stop.'
