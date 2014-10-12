import numpy as np

import viscojapan as vj
from viscojapan.utils import assert_assending_order

class SeafloorPatch(object):
    def __init__(self, file_sites_seafloor):
        self.file_sites_seafloor = file_sites_seafloor
        self._parse_sites_seafloor()

    def _parse_sites_seafloor(self):
        tp = np.loadtxt(self.file_sites_seafloor,'4a, 4a, 2f, 3f, d')
        self.sites_seafloor = [ii[1] for ii in tp]
        assert_assending_order(self.sites_seafloor)
        
        self.disp_seafloor = np.vstack([ii[3] for ii in tp]).reshape([-1,1])
        self.sites_seafloor_pos = {ii[1]:ii[2] for ii in tp}
        

    def _patch_epochal_data(self, patch_array, file_org, file_patched):
        assert len(patch_array) == len(self.sites_seafloor)*3
        obs_obj = vj.EpochalData(file_org)
        obs_obj_with_seafloor = vj.EpochalData(file_patched)

        epochs = obs_obj.get_epochs()
        for epoch in epochs:
            obs_patched = np.vstack([obs_obj(epoch), patch_array])
            obs_obj_with_seafloor[epoch] = obs_patched.reshape([-1,1])
        obs_obj_with_seafloor['sites'] = \
            list(obs_obj['sites']) + self.sites_seafloor
        obs_obj_with_seafloor['sites_seafloor'] = self.sites_seafloor
        obs_obj_with_seafloor['value_seafloor'] = patch_array
        

    def patch_disp(self, file_disp, file_patched):
        self._patch_epochal_data(self.disp_seafloor, file_disp, file_patched)

    def patch_sd(self, file_sd, file_patched):
        INF = 1e99
        sd = np.zeros_like(self.disp_seafloor)+INF
        self._patch_epochal_data(sd, file_sd, file_patched)

    def patch_sites(self, file_sites, file_patched):
        tp = np.loadtxt(file_sites,'4a, 2f')
        sites = [ii[0] for ii in tp]
        sites_pos = {ii[0]:ii[1] for ii in tp}
        sites_with_seafloor = sites + self.sites_seafloor
        assert_assending_order(sites_with_seafloor)
        pos_dic = dict(list(sites_pos.items()) + \
                       list(self.sites_seafloor_pos.items()))

        with open(file_patched, 'wt') as fid:
            fid.write('# sites are ordered by names. Sites start with an underscore are seafloor sites.\n')
            fid.write('# num of sites: %d\n'%len(sites_with_seafloor))
            fid.write('# num of seafloor sites: %d\n'%len(self.sites_seafloor))
            fid.write('# site lon lat\n')
            for site in sites_with_seafloor:
                lon, lat = pos_dic[site]
                fid.write('%s %f %f\n'%(site.decode(), float(lon), float(lat)))

        
        
        

    
