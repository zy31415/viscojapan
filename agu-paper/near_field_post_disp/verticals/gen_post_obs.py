import viscojapan as vj

reader = vj.inv.ep.EpochDisplacement('../cumu_post_with_seafloor.h5')
post = reader.get_post_at_epoch(1344)

sites = reader.get_mask_sites()
pos = vj.sites_db.get_pos_dic()


with open('share/post_ver_1344_obs', 'wt') as fid:
    for d, s in zip(post, sites):
        lon, lat = pos[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, 0, d[2], s))
