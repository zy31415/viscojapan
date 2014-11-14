import os

def _assert_file_name_extension(fn, ext):
    fn, ext_ = os.path.splitext(fn)
    assert ext_ == ext, '%s == %'%(ext_, ext)
