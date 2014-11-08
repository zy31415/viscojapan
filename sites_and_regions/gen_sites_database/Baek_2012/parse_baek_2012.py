import viscojapan as vj

__doc__=''' This scirpt parse Baek 2012 supplemental table
into two file: sites_network and sites_position
'''

# generate position file
pos_dic = {}
sites_IGSSTA = []
sites_KOREAN = []
with open('Baek_2012_supp_TableS1.txt', 'r') as fid:
    for ln in vj.next_non_commenting_line(fid):
        site, lon, lat, *_ = ln.split()
        site = site.strip()
        if len(site)==5:
            site = site[1:]
            sites_IGSSTA.append(site)
        else:
            sites_KOREAN.append(site)
        assert len(site)==4
        pos_dic[site] = (float(lon), float(lat))

with open('sites_position', 'w') as fid:
    fid.write('# site lon lat\n')
    for site in sorted(pos_dic):
        tp = pos_dic[site]
        fid.write('%s %f %f Beak_2012\n'%(site,tp[0], tp[1]))

with open('sites_network', 'w') as fid:
    fid.write('# site network\n')
    for site in sorted(sites_KOREAN):
        fid.write('%s KOREAN Beak_2012\n'%(site))
    for site in sorted(sites_IGSSTA):
        fid.write('%s IGSSTA Beak_2012\n'%(site))
