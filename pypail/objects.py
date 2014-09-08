class Object(object):
    """
    Generic object returned by the API.

    Each class that derives from this one declares a number of attributes that
    are used to navigate the data returned by the API. For example, Droplet
    objects contain an embedded Region, which contains one or more Sizes.
    """

    _EMBED = {}  # derived classes override these
    _FETCH = {}
    _DATES = []

    def __init__(self, credentials, data=None):
        self._credentials, self._data = credentials, data

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __getattr__(self, key):
        if key in self._EMBED:
            return self._EMBED[key]()(self._credentials, self._data[key])
        elif key in self._FETCH:
            return self._fetch(
                self._FETCH[key]['endpoint'](self),
                self._FETCH[key]['class'](),
            )
        return self._data[key]

    def _fetch(self, endpoint, class_):
        for data in self._credentials.request(endpoint)[class_._MULTIPLE_KEY]:
            yield class_(self._credentials, data)


class Account(Object):

    _FETCH = {
        'droplets': {
            'endpoint': lambda x: '/droplets',
            'class': lambda: Droplet,
        },
    }


class Droplet(Object):

    _SINGLE_KEY = 'droplet'
    _MULTIPLE_KEY = 'droplets'

    _EMBED = {
        'image': lambda: Image,
        'kernel': lambda: Kernel,
        'region': lambda: Region,
        'size': lambda: Size,
    }

    _DATES = ['created_at']


class Image(Object):
    pass


class Kernel(Object):
    pass


class Region(Object):
    pass


class Size(Object):
    pass
