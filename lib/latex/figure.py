import sys
import tempfile
import subprocess
import os
from os.path import basename

__all__ = ['Latex', 'LatexDoc', 'Figure', 'Subfigure', 'PDFComplie','VSpace',
           'NextParagraph']

class Latex(object):
    def __init__(self):
        self.elements = []

    def print(self, file=sys.stdout):
        for ele in self.elements:
            ele.print(file=file)

class LatexDoc():
    def __init__(self):
        self.elements = []

    def print(self, file=sys.stdout):
        print('\\documentclass[11pt,letterpaper]{article}',
              file = file)

        print('\\usepackage[letterpaper,margin=10mm]{geometry}',
              file = file)        
        
        print('''
\\usepackage{graphicx}
\\usepackage{caption}
\\usepackage{subcaption}
''', file = file)
        
        print('\\begin{document}',
              file = file)
        print('\\pagenumbering{gobble}', file=file)
        for ele in self.elements:
            ele.print(file=file)

        print('\\end{document}',
              file = file)

class Figure(object):
    def __init__(self,
                 caption = None,
                 label = None,
                 if_continued = False):
        self._subfigures = []

        self.caption = caption
        self.label = label

        self.if_continued = if_continued

    def append_subfigure(self, sub):
        self._subfigures.append(sub)

    def print(self, file=sys.stdout):
        self._print_prefix(file=file)        
        for subf in self._subfigures:
            subf.print(file=file)
        self._print_suffix(file=file)        

    def _print_prefix(self, file=sys.stdout):
        print('''\\begin{figure}[h]
    \\centering''', file=file)
        if self.if_continued:
            print('''    \\ContinuedFloat''', file=file)

    def _print_suffix(self, file=sys.stdout):
        if self.caption is not None:
            print('\\caption{{{caption}}}'.format(caption=self.caption),
                  file = file)

        if self.label is not None:
            print('\\label{{{label}}}'.format(label=self.label),
                  file = file)
        print('\\end{figure}', file=file)
        
class Subfigure(object):
    def __init__(self,
                 subfig_width,
                 trim,
                 file,
                 incl_width = 1.,
                 caption = None,
                 rotation = 0):
        self.subfig_width = subfig_width
        self.incl_width = incl_width
        self.trim = trim
        self.file = file
        self.caption = caption
        self.rotation = rotation
        
    def print(self, file=sys.stdout):
        print('\\begin{{subfigure}}[b]{{{width}\\textwidth}}'.format(width = self.subfig_width),
              file = file)
        
        print('''\\centering
\\includegraphics[width={incl_width}\\textwidth, clip=true, trim={trim[0]} {trim[1]} {trim[2]} {trim[3]}, angle={rotation}]{{{file}}}'''.format(
            incl_width = self.incl_width,
            trim = self.trim,
            file = self.file,
            rotation = self.rotation),
              file = file)

        if self.caption is not None:
            print('\\caption{{{caption}}}'.format(caption = self.caption),
                  file = file)
        
        print('\\end{subfigure}',
              file = file)
        
class VSpace(object):
    def __init__(self,
                 size = '10mm'):
        self.size = size
        
    def print(self, size='10mm', file=sys.stdout):
        print('\\vspace{{{size}}}'.format(size=self.size), file=file)

class NextParagraph(object):
    def __init__(self):
        pass
        
    def print(self, file=sys.stdout):
        print('\n\n', file=file)
        
class PDFComplie(object):
    def __init__(self,
                 latex
                 ):
        self.latex = latex

    def compile(self, out_file):
        fid = tempfile.NamedTemporaryFile(mode='w+t', dir='./')
        self.latex.print(fid)
        fid.seek(0)

        p = subprocess.Popen(
            ['pdflatex', fid.name],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            )
        
        self.stdout, self.stderr = p.communicate()
        
        if p.returncode != 0:
            print(self.stderr.decode())
            print(self.stdout.decode())
            raise Exception('Command returned an error.')
        
        base_name = basename(fid.name)
        fid.close()
        self._clean(base_name)
        os.rename(base_name+'.pdf', out_file)

    def _clean(self, basename):
        os.remove(basename + '.aux')
        os.remove(basename + '.log')
        
            
