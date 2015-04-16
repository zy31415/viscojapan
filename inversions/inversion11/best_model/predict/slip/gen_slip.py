import viscojapan as vj

reader = vj.inv.ResultFileReader('../outs/nrough_06_naslip_11.h5')
slip = reader.get_slip()

slip.save('slip.h5')
