import viscojapan as vj

writer = vj.tsana.ObservationDatatbaseWriter()
writer.create_database()
writer.insert_cumu_linres()
writer.insert_cumu_obs_tsm()
writer.insert_seafloor_original()
