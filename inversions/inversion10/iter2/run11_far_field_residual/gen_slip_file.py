import viscojapan as vj

reader = vj.inv.ResultFileReader('../run11/outs/nrough_06_naslip_11.h5')

reader.get_slip().save('slip.h5')

reader.get_pred_disp().save('pred_disp.h5')
reader.get_obs_disp().save('obs_disp.h5')
