import numpy as np

import tenv_file_reader as tenv

res = tenv.read_tenv_file('./J550.IGS08.tenv')

for ri in res:
    print(ri['site'])
