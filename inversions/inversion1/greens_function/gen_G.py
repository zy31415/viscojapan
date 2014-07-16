from glob import glob

from viscojapan.pollitz import PollitzOutputsToEpochalData

from epochs import epochs

num_subflts = len(glob('outs/day_0000_flt_????.out'))

#epochs.remove(1020)

gen = PollitzOutputsToEpochalData(
    epochs = epochs,
    G_file = 'G.h5',
    num_subflts = num_subflts,
    pollitz_outputs_dir = 'outs',
    sites_file = 'sites_with_seafloor',
    )
gen()
