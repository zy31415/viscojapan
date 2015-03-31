import viscojapan as vj

reader = vj.EpochalSitesFileReader('cumu_post_with_seafloor.h5')

co = reader[0].reshape([-1, 3])
sites = reader.filter_sites

pos = vj.sites_db.get_pos_dic()


with open('co_obs', 'wt') as fid:
    for d, s in zip(co, sites):
        lon, lat = pos[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))
