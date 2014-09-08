class Object(object):
    """
    Generic object returned by the API.

    Each class that derives from this one declares a number of attributes that
    are used to navigate the data returned by the API. For example, Droplet
    objects contain an embedded Region, which contains one or more Sizes.
    """

    def __init__(self, credentials, data=None):
        self._credentials, self._data = credentials, data

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __getattr__(self, key):
        return self._data[key]

    def fetch(self, endpoint, class_):
        for data in self._credentials.request(endpoint)[class_.MULTIPLE_KEY]:
            yield class_(self._credentials, data)


class Account(Object):

    @property
    def droplets(self):
        return self.fetch('/droplets', Droplet)


class Droplet(Object):

    SINGLE_KEY = 'droplet'
    MULTIPLE_KEY = 'droplets'
