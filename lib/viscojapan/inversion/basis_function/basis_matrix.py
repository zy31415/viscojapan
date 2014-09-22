from numpy import arange, asarray, dot, hstack
import scipy.sparse as sparse

from viscojapan.fault_model import FaultFileIO
from .cubic_b_splines import CubicBSplines

__all__ = ['BasisMatrix','BasisMatrixBSpline']

class BasisMatrix(object):
    def __init__(self,
                 num_subflts,
                 num_epochs = 1
                 ):

        self.num_subflts = num_subflts
        self.num_epochs = num_epochs

    def gen_basis_matrix_sparse(self):
        return sparse.eye(self.num_subflts*self.num_epochs)

    @staticmethod
    def create_from_fault_file(fault_file, num_epochs = 1):
        fid = FaultFileIO(fault_file)                

        spline_obj = BasisMatrix(
            num_subflts = fid.num_subflt_along_strike * fid.num_subflt_along_dip,
            num_epochs = num_epochs
            )
        return spline_obj

    def __call__(self):
        return self.gen_basis_matrix_sparse()
        

class BasisMatrixBSpline(BasisMatrix):
    def __init__(self,
                 dx_spline,
                 xf,
                 dy_spline,
                 yf,
                 num_epochs = 1
                 ):

        self.dx_spline = dx_spline
        self.xf = xf
        self.dy_spline = dy_spline
        self.yf = yf
        self.num_epochs = num_epochs

    def _spline(self, sj, ds, j):

        spl = CubicBSplines(ds)
        _, slip = spl.b_spline_over_sections(sj, j)

        return slip

    def _gen_x_slip(self, m):
        return self._spline(self.xf, self.dx_spline, m)

    def _gen_y_slip(self, n):
        return self._spline(self.yf, self.dy_spline, n)


    def gen_slip_mesh(self, m, n):
        xslip = self._gen_x_slip(m)
        yslip = self._gen_y_slip(n)
        
        xslip = asarray([xslip])
        yslip = asarray([yslip])

        slip = dot(yslip.T, xslip)

        return slip

    def gen_basis_matrix(self):
        res = []
        for nth, _ in enumerate(self.yf[0:-1]):
            for mth, _ in enumerate(self.xf[0:-1]):            
                slip = self.gen_slip_mesh(mth, nth)
                res.append(slip.reshape([-1,1]))
        res1 = sparse.csr_matrix(hstack(res))
        res2 = sparse.block_diag([res1]*self.num_epochs)
        return res2

    def gen_basis_matrix_sparse(self):
        return sparse.csr_matrix(self.gen_basis_matrix())

    @staticmethod
    def create_from_fault_file(fault_file, num_epochs = 1):
        fid = FaultFileIO(fault_file)                

        dx = fid.subflt_sz_strike
        dy = fid.subflt_sz_dip
        
        x_f = fid.x_f
        y_f = fid.y_f

        spline_obj = BasisMatrix(
            dx_spline = dx,
            xf = x_f,
            dy_spline = dy,
            yf = y_f,
            num_epochs = num_epochs
            )
        return spline_obj

    def __call__(self):
        return self.gen_basis_matrix_sparse()
    
            

            



            
            
