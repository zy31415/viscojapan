import os

class Plotter(object):
    def __init__(self):
        self.trash_files = ['gmt.conf', 'gmt.history']
        
    def plot(self, output_file):
        self.output_file = output_file

    def clean(self):
        self.trash_files.append('.'.join(self.output_file.split('.')[:-1]+['ps']))

        for file in self.trash_files:
            if os.path.exists(file):
                os.remove(file)
