import collections

from .site import Site

__all__=['Sites']

def _is_Site(obj):
    assert isinstance(obj, Site), 'Must be Site object.'

class Sites(collections.UserList):
    def __init__(self, *args, **kwargs):
        for ii in args[0]:
            _is_Site(ii)

        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        _is_Site(value)
        super().__setitem__(key, value)

    def save_to_txt(self, fn,
                    cols='id lon lat',
                    header=None):
        with open(fn, 'wt') as fid:
            if header is not None:
                fid.write(header)
                if header[-1] != '\n':
                    fid.write('\n')
            fid.write('# ' + cols +'\n')
            formats = cols.split()
            for site in self:
                for fm in formats:
                    val = getattr(site, fm)
                    fid.write('{val}  '.format(val=val))
                fid.write('\n')

    @property
    def lons(self):
        return [site.lon for site in self]

    @property
    def lats(self):
        return [site.lat for site in self]

    @property
    def max_lon(self):
        return max(self.lons)

    @property
    def max_lat(self):
        return max(self.lats)

    @property
    def min_lon(self):
        return min(self.lons)

    @property
    def min_lat(self):
        return min(self.lats)

    def __str__(self):
        num = len(self)
        head = ['Sites list (# %d):'%num]
        body = []
        for nth, site in enumerate(self):
            body.append('  ' + str(site))

        if len(body)>16:
            body = body[:10] + ['  ...'] + body[-5:]

        out = '\n'.join(head + body)
        return out
                
