import scipy.optimize as op
import h5py
import numpy as np

from ..epoch_3d_array import Slip

__author__ = 'zy'
__all__ = ['SlipExtrapolationEXP', 'SlipExtrapolationLOG']

def f_log(t, co, b, tau):
    t = np.asarray(t)
    tau = np.abs(tau)
    return co + b * np.log10(1+t/tau)

def f_exp(t, co, b, tau):
    t = np.asarray(t)
    tau = np.abs(tau)
    return co + b * (1 - np.exp(-t/tau))

def estimate_initial_values(s):
    co0 = s[0]
    b0 = s[-1] - s[0]
    tau0 = 100
    return co0, b0, tau0


def curve_fit_exp(epochs, s):
    init0 = estimate_initial_values(s)
    popt, pcov = op.curve_fit.curve_fit(
        f = f_exp,
        xdata = epochs,
        ydata = s,
        p0 = init0,
    )

    return popt

def curve_fit_log(epochs, s):
    init0 = estimate_initial_values(s)
    popt, pcov = op.curve_fit.curve_fit(
        f = f_log,
        xdata = epochs,
        ydata = s,
        p0 = init0,
    )

    return popt


class SlipExtrapolation(object):
    HDF5_DATASET_NAME_FOR_3D_ARRAY = Slip.HDF5_DATASET_NAME_FOR_3D_ARRAY

    def __init__(self, slip,
                  epochs,
                  output_file):
        self.slip = slip
        self.num_subflt_along_dip = slip.num_subflt_along_dip
        self.num_subflt_along_strike = slip.num_subflt_along_strike

        self.epochs = epochs
        self.num_epochs = len(self.epochs)

        self._init_hdf5_file(output_file)

        self.maxfev = 10000


    def _init_hdf5_file(self, output_file):
        shape = (self.num_epochs, self.num_subflt_along_dip, self.num_subflt_along_strike)

        fid = h5py.File(output_file, 'w')
        fid.create_dataset(name = self.HDF5_DATASET_NAME_FOR_3D_ARRAY,
                           shape = shape,
                           dtype = float)

        fid.create_dataset(name = 'tau',
                           shape = (shape[1], shape[2]),
                           dtype = float)

        fid['epochs'] = self.epochs

        self.fid = fid

        self.data = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY]
        self.tau = fid['tau']

    def _curve_fit(self, epochs, s):
        init0  = estimate_initial_values(s)
        popt, pcov = op.curve_fit(
            f = self._func,
            xdata = epochs,
            ydata = s,
            p0 = init0,
            maxfev = self.maxfev
            )
        return popt


    @staticmethod
    def _func(x, *args):
        pass

    def _model(self, nth_alg_dip, nth_alg_strike):

        s = self.slip.get_cumu_slip_at_subfault(nth_alg_dip, nth_alg_strike)
        epochs = self.slip.get_epochs()

        popt = self._curve_fit(epochs, s)

        y_pred = self._func(self.epochs, *popt)

        self.data[:,nth_alg_dip, nth_alg_strike] = y_pred

        tau = popt[2]
        self.tau[nth_alg_dip, nth_alg_strike] = tau



    def go(self):
        for ndip in range(self.num_subflt_along_dip):
            for nstk in range(self.num_subflt_along_strike):
                # print('Subflt:',ndip, nstk)
                self._model(ndip, nstk)

        self.fid.close()


class SlipExtrapolationEXP(SlipExtrapolation):
    def __init__(self, slip,
                  epochs,
                  output_file):
        super().__init__(slip=slip,
                         epochs = epochs,
                         output_file = output_file)

    @staticmethod
    def _func(x, *args):
        return f_exp(x, *args)


class SlipExtrapolationLOG(SlipExtrapolation):
    def __init__(self,
                  slip,
                  epochs,
                  output_file):
        super().__init__(slip=slip,
                         epochs = epochs,
                         output_file = output_file)
    @staticmethod
    def _func(x, *args):
        return f_log(x, *args)



