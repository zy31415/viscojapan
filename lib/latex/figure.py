import sys

__all__ = ['Figure', 'Subfigure']

class Figure(object):
    def __init__(self,
                 caption = None,
                 label = None,
                 if_continued = False):
        self._subfigures = []
        if caption is None:
            self.caption = ''
        else:
            self.caption = caption

        if label is None:
            self.label = ''
        else:
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
        print('''    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{figure}}'''.format(
    caption = self.caption,
    label = self.label),
              file=file)
        
class Subfigure(object):
    def __init__(self,
                 width,
                 trim,
                 file):
        self.width = width
        self.trim = trim
        self.file = file
    def print(self, file=sys.stdout):
        print('''    \\begin{{subfigure}}[b]{{{width}\\textwidth}}
        \\centering
        \\includegraphics[width=1.0\\textwidth, clip=true, trim={trim[0]} {trim[1]} {trim[2]} {trim[3]}]{{{file}}}
    \\end{{subfigure}}'''.format(
        width = self.width,
        trim = self.trim,
        file = self.file),
              file = file)
