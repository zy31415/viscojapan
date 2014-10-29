import numpy as np

import viscojapan as vj

patch = vj.tsana.SeafloorPatch('sites_seafloor')
print("Patch disp ...")
patch.patch_disp('../post_fit/cumu_post.h5',
                 'cumu_post_with_seafloor.h5')
##print("Patch sd ...")
##patch.patch_sd('../sd/sd.h5', 'sd_with_seafloor.h5')

print("Patch sites list ...")
patch.patch_sites('../post_fit/sites/sites','sites_with_seafloor')

    
