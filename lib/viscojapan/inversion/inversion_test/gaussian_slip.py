import sys

from ...fault_model import FaultFileReader

from numpy import arange, meshgrid, exp, log

class GaussianSlip(object):
    def __init__(self,
                 num_subflts_in_dip,
                 num_subflts_in_strike,
                 ):
        self.num_subflts_in_dip = num_subflts_in_dip
        self.num_subflts_in_strike = num_subflts_in_strike
        
        # spatial shape
        self.mu_dip = 4.
        self.mu_stk = 12.
        self.sig_dip = 2
        self.sig_stk = 5

        # temporal part
        self.max_slip0 = 10.
        self.log_mag = 1.
        self.tau = 5.

    def __call__(self,t):
        x = arange(self.num_subflts_in_strike)
        y = arange(self.num_subflts_in_dip)

        x, y = meshgrid(x,y)

        self.x = x
        self.y = y

        mu_x = self.mu_stk
        mu_y = self.mu_dip

        sig_x = self.sig_stk
        sig_y = self.sig_dip

        z = exp(-(x-mu_x)**2/(2*sig_x**2))*exp(-(y-mu_y)**2/(2*sig_y**2))
        z *= self.max_slip(t)

        return z

    def max_slip(self, t):        
        return self.max_slip0 + self.log_mag*log(1.+t/self.tau)

    @staticmethod
    def create_from_fault_file(fault_file):
        fio = FaultFileReader(fault_file)
        return GaussianSlip(
            num_subflts_in_dip = fio.num_subflt_along_dip,
            num_subflts_in_strike = fio.num_subflt_along_strike
            )
        
