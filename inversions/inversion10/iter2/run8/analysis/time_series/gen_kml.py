import viscojapan as vj

kml = vj.inv.KMLShowTimeSeries(
    file_sites = 'sites_with_seafloor',
    db_pred = '../pred_disp/~pred_disp.db'
    )
kml.save_kml('time_series.kml')
kml.plot(file_ext = 'pdf', nproc=6)
kml.plot(file_ext = 'png', nproc=6)

