__all__ = ['FileIOBase']

class FileIOBase(object):
    def __init__(self,
                 file_name):        
        self.file_name = file_name
        self.fid = self.open()

    def open(self):
        raise NotImplementedError(''' Do these things here:
(1) Check if file exists / not exists.
(2) open the file with proper opener.
''')
    
    def close(self):
        if self.fid is not None:
            self.fid.close()
        self.fid = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()
