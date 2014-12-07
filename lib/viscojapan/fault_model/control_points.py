__all__=['control_points1','control_points2', 'control_points3']

class ControlPoints(object):
    def __init__(self,
                 B0,
                 FLT_SZ_DIP ,
                 DIP_D ,
                 STRIKE,
                 Y_PC,
                 Y_FC,
                 DEP0):
        self.B0 = B0
        self.FLT_SZ_DIP = FLT_SZ_DIP
        self.DIP_D = DIP_D
        self.STRIKE = STRIKE
        self.Y_PC = Y_PC
        self.Y_FC = Y_FC
        self.DEP0 = DEP0

# The eastern edge is aligned with the trench.
control_points1 = ControlPoints(
    B0 = (144.697756238647, 40.25451048457508),
    FLT_SZ_DIP = 425.,
    DIP_D = [10.,14.,22.,28.],
    STRIKE = 195.,
    Y_PC = [0,98.480775301220802,171.25295477192054,
            217.61214750025991, 394.20166607204533],
    Y_FC = [0,100.,175.,225.,425.],
    DEP0 = 3.
    )        

# The eastern edge is in the east of the trench
control_points2 = ControlPoints(
    B0 = (145.03801505694778, 40.18408337695884),
    FLT_SZ_DIP = 425.,
    DIP_D = [7.7,14.,22.,28.],
    STRIKE = 195.,
    Y_PC = [0, 128.480775301220802, 201.25295477192054,
            247.61214750025991, 424.20166607204533],
    Y_FC = [0, 129.864134, 204.864134, 254.864134, 454.864134],
    DEP0 = 3.
    )

# For better deeper part of fault, adjust the dip of the deepest
#    part of the fault model.
control_points3 = ControlPoints(
    B0 = (145.03801505694778, 40.18408337695884),
    FLT_SZ_DIP = 425.,
    DIP_D = [7.7,14.,22.,23.],
    STRIKE = 195.,
    Y_PC = [0, 128.480775301220802, 201.25295477192054,
            247.61214750025991, 424.20166607204533],
    Y_FC = [0, 129.864134, 204.864134, 254.864134, 454.864134],
    DEP0 = 3.
    )
