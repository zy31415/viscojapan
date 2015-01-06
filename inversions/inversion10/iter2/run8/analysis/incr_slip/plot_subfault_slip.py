import viscojapan as vj

plt = vj.inv.FaultSlipPlotter(
    '../../outs/nrough_06_naslip_10.h5',
    '../../../fault_model/fault_bott80km.h5'
    )

plt.plot('fault_slip.pdf')
