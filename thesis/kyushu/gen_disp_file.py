import viscojapan as vj

with vj.EpochalFileReader(
    '../../tsana/post_fit/cumu_post_with_seafloor.h5') as reader:
    reader['']
