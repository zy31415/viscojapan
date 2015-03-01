import viscojapan as vj

kml = vj.inv.KMLShowTimeSeries(
    file_sites = 'sites_with_seafloor',
    result_file = '../../outs/best_result.h5',
    partition_file = '../deformation_partition/deformation_partition.h5'
    )
kml.save_kml('time_series.kml')
#kml.plot(file_ext = 'pdf', nproc=3)
kml.plot(file_ext = 'png', nproc=3)

