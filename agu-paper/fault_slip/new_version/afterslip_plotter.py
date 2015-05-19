import viscojapan as vj

result_file = 'nrough_06_naslip_11.h5'
fault_file = 'fault_bott80km.h5'

cpt_file = 'Blues_09.cpt'
cpt_file = 'hot'
cpt_reverse = True

slip = vj.inv.ResultFileReader(result_file).get_slip()

epochs = list(range(0,450,50))

plotter = vj.inv.AfterslipPlotter(
    slip = slip,
    epochs = epochs,
    fault_file = fault_file,
    cpt_file = cpt_file,
    cpt_reverse = cpt_reverse
)

plotter.plot()

plotter.save('test_.pdf')


