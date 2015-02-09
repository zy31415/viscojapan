import viscojapan as vj

sites = vj.sites_db.SitesDB().gets_from_txt_file('sites_with_seafloor')
sites.save_to_txt('sites.gmt', cols='lon lat name id')
