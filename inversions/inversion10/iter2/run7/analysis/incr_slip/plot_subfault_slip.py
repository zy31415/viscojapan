import viscojapan as vj

plt = vj.inv.FaultSlipPlotter(
    '../../outs/nrough_05_naslip_11.h5',
    '../../../fault_model/fault_bott80km.h5'
    )

plt.plot('fault_slip.pdf',
         if_x_log=False,
         xlim=[0, 1344],
         ylim=[0,80],
         yticks=[20,40,60],
         xticks = [500, 1000],
         xticklabels = [r'500', r'1000'],
         )

