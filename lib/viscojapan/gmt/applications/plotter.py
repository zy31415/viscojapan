import os
import pGMT

class Plotter(object):
    def __init__(self):
        self.gmt = pGMT.GMT()
        self.gplt = self.gmt.gplt
        
    def plot(self, output_file):
        raise NotImplemented()

    def save(self, output_file):
        self.output_file = output_file
        self.gmt.gplt.finish()
        self.gmt.save(output_file)
