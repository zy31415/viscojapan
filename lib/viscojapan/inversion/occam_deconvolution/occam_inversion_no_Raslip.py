from ..epoch_file_reader_for_inversion import EpochGNoRaslip

from .occam_deconvolution import OccamDeconvolution

__all__ = ['OccamInversionNoRaslip']


class OccamInversionNoRaslip(OccamDeconvolution):
    def __init__(self,
                 file_G0,
                 files_Gs,
                 nlin_par_names,
                 file_d,
                 file_sd,
                 sites,
                 epochs,                 
                 regularization,
                 basis,
                 file_slip0,
                 decreasing_slip_rate = True,
                 ):

        super().__init__(file_G0 = file_G0,
                 files_Gs = files_Gs,
                 nlin_par_names = nlin_par_names,
                 file_d = file_d,
                 file_sd = file_sd,
                 sites = sites,
                 epochs = epochs,
                 regularization = regularization,
                 basis = basis,
                 file_slip0 = file_slip0,
                 decreasing_slip_rate = decreasing_slip_rate,
                 )

    def _init_Gs(self, file_G0, files_Gs, sites):
        self.G0 = EpochGNoRaslip(file_G0, sites)
        self.num_subflts = self.G0.get_num_subflts()
        self.Gs = [EpochGNoRaslip(f, sites) for f in files_Gs]

