import viscojapan as vj

writer = vj.tsana.ObservationDatatbaseWriter()
writer.create_database()
writer.insert_linres()
writer.insert_cumu_post_displacement()
writer.insert_seafloor_original()
