import numpy as np

from ...epochal_data import EpochalSitesFileReader, EpochalFileReader, \
     DiffED, EpochalG, EpochalIncrSlipFileReader
from ...utils import as_string

__all__ =['DeformPartitioner']
__author__ = 'zy'


class DeformPartitioner(object):
    def __init__(self,
                 file_G0,
                 epochs,
                 slip,
                 files_Gs = None,
                 nlin_pars = None,
                 nlin_par_names = None,
                 file_incr_slip0 = None,
                 ):

        self.epochs = epochs
        self.num_epochs = len(self.epochs)

        self.file_G0 = file_G0
        self.file_G0_reader = EpochalSitesFileReader(
            epoch_file = self.file_G0,
            )

        self.slip = slip

        self.files_Gs = files_Gs

        self._assert_all_G_files_have_the_same_sites_list()

        self.sites_for_prediction = self.file_G0_reader.filter_sites

        self.nlin_par_vals = nlin_pars
        self.nlin_par_names = nlin_par_names
        self.file_incr_slip0 = file_incr_slip0
        self._check_incr_slip0_file_spacing()

        if self.files_Gs is not None:
            self._get_delta_nlin_pars()


    def _assert_all_G_files_have_the_same_sites_list(self):
        reader = EpochalFileReader(self.file_G0)
        sites = as_string(reader['sites'])

        for G in self.files_Gs:
            reader = EpochalFileReader(G)
            assert sites == as_string(reader['sites'])

    def _check_incr_slip0_file_spacing(self):
        reader  = EpochalIncrSlipFileReader(self.file_incr_slip0)
        assert reader.epochs == self.epochs, \
               '''Epochs of initial slip input is the same as that is in the result file
{slip0}
{result}
'''.format(slip0 = reader.epochs, result=self.epochs)

    def _get_delta_nlin_pars(self):
        self.delta_nlin_pars = []
        for name, par in zip(self.nlin_par_names, self.nlin_par_vals):
            delta = par - self.file_G0_reader[name]
            self.delta_nlin_pars.append(delta)


    def E_cumu_slip(self, nth_epoch):
        cumuslip = self.slip.get_cumu_slip_at_nth_epoch(nth_epoch).reshape([-1,1])
        G0 = self.file_G0_reader[0]
        disp = np.dot(G0, cumuslip)
        if self.files_Gs is not None:
            disp += self._nlin_correction_E_cumu_slip(nth_epoch)
        return disp

    def _nlin_correction_E_cumu_slip(self, nth_epoch):
        reader = EpochalIncrSlipFileReader(self.file_incr_slip0)

        slip0 = reader.get_cumu_slip_at_nth_epoch(nth_epoch)

        dGs = []
        for file_G, par in zip(self.files_Gs, self.nlin_par_names):
            G0 = EpochalG(self.file_G0)
            G = EpochalG(file_G)
            diffG = DiffED(ed1=G0, ed2=G, wrt=par)
            dGs.append(diffG[0])

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr


    def E_co(self):
        return self.E_cumu_slip(0)

    def E_aslip(self, nth_epoch):
        return self.E_cumu_slip(nth_epoch) - self.E_co()

    def R_nth_epoch(self, from_nth_epoch, to_epoch):
        epochs = self.epochs
        from_epoch = epochs[from_nth_epoch]

        del_epoch = to_epoch - from_epoch
        del_epoch = int(del_epoch)

        if del_epoch <= 0:
            return np.zeros([self.file_G0_reader[0].shape[0],1])

        G = self.file_G0_reader[del_epoch] - self.file_G0_reader[0]
        s = self.slip.get_incr_slip_at_nth_epoch(from_nth_epoch).reshape([-1,1])
        disp = np.dot(G, s)
        if self.files_Gs is not None:
            corr = self._nlin_correction_R_nth_epoch(from_nth_epoch, to_epoch)
            disp += corr
        return disp

    def _nlin_correction_R_nth_epoch(self, from_nth_epoch, to_epoch):
        from_epoch = int(self.epochs[from_nth_epoch])
        reader = EpochalIncrSlipFileReader(self.file_incr_slip0)
        slip0 = reader[from_epoch]

        del_epoch = int(to_epoch - from_epoch)

        dGs = []
        for file_G, par in zip(self.files_Gs, self.nlin_par_names):
            G0 = EpochalG(self.file_G0)
            G = EpochalG(file_G)
            diffG = DiffED(ed1=G0, ed2=G, wrt=par)
            dG0 = diffG[0]
            dG = diffG[del_epoch]
            dGs.append(dG-dG0)

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr

    def R_co(self, epoch):
        return self.R_nth_epoch(0, epoch)

    def R_co_at_nth_epoch(self, nth):
        return self.R_co(self.epochs[nth])

    def R_aslip(self, epoch):
        num_epochs = self.num_epochs
        disp = None
        for nth in range(num_epochs):
            if nth == 0:
                continue
            if disp is None:
                disp = self.R_nth_epoch(nth, epoch)
            else:
                arr = self.R_nth_epoch(nth, epoch)
                disp += arr
        return disp

    def R_aslip_at_nth_epoch(self, nth):
        return self.R_aslip(self.epochs[nth])