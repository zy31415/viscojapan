import viscojapan as vj

ep = vj.EpochalDisplacement('cumu_post_with_seafloor.h5')

disp_co = ep[0]
epochs = ep.get_epochs()

ep2 = vj.EpochalData('post_obs.h5')

for epoch in epochs:
    print(epoch)
    disp = disp_co - ep[epoch]
    ep2[epoch] = disp
    
ep2.copy_info_from('cumu_post_with_seafloor.h5')

