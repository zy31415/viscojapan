import viscojapan as vj

result_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5'
cpt_file = ''

slip = vj.inv.ResultFileReader(result_file).get_slip()

ts = [0, 44, 89, 134, 179, 224, 268, 313, 358]

plotter = vj.inv.AfterslipPlotter(
    slip = slip,
    epochs= ts,
    fault_file = fault_file,
)


plotter.plot()

plotter.save('test_.pdf')


