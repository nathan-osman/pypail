from dateutil.parser import parse


class Object(object):
    """
    Generic object returned by the API.

    Each class that derives from this one declares a number of attributes that
    are used to navigate the data returned by the API. For example, Droplet
    objects contain an embedded Region, which contains one or more Sizes.
    """

    _SPECIAL = {}  # derived classes override this

    def __init__(self, credentials, data=None):
        self._credentials, self._data = credentials, data

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __getattr__(self, key):
        return self._SPECIAL[key](self) if key in self._SPECIAL else self._data[key]

    def _date(self, key):
        """
        Convert an ISO 8601 date to datetime.
        """
        return parse(self._data[key])

    def _filter(self, endpoint, class_, key, condition):
        """
        Return a generator that filters based on a condition.
        """
        for item in self._multi(endpoint, class_, key):
            if condition(item):
                yield item

    def _multi(self, endpoint, class_, key):
        """
        Return a generator for items at the specified endpoint.
        """
        for item in self._credentials.request(endpoint)[key]:
            yield class_(self._credentials, item)

    def _single(self, class_, key):
        """
        Return an embedded instance of the specified class.
        """
        return class_(self._credentials, self._data[key])


class Account(Object):

    _SPECIAL = {
        'actions': lambda x: x._multi('/actions', Action, 'actions'),
        'domains': lambda x: x._multi('/domains', Domain, 'domains'),
        'droplets': lambda x: x._multi('/droplets', Droplet, 'droplets'),
        'images': lambda x: x._multi('/images', Image, 'images'),
        'keys': lambda x: x._multi('/account/keys', SSHKey, 'ssh_keys'),
        'regions': lambda x: x._multi('/regions', Region, 'regions'),
        'sizes': lambda x: x._multi('/sizes', Size, 'sizes'),
    }


class Action(Object):

    _SPECIAL = {
        'completed_at': lambda x: x._date('completed_at'),
        'region': lambda x: x._filter('/regions', Region, 'regions', lambda y: x._data['region'] == y.slug).next(),
        'started_at': lambda x: x._date('started_at'),
    }

    # TODO: implement a 'resource' property that automatically
    # fetches the appropriate resource based on ID and type


class Backup(Object):

    pass


class Domain(Object):

    _SPECIAL = {
        'records': lambda x: x._multi('/domains/%s/records' % x.name, DomainRecord, 'domain_records'),
    }


class DomainRecord(Object):

    pass


class Droplet(Object):

    _SPECIAL = {
        'actions': lambda x: x._multi('/droplets/%d/actions' % x.id, Action, 'actions'),
        'backups': lambda x: x._multi('/droplets/%d/backups' % x.id, Backup, 'backups'),
        'created_at': lambda x: x._date('created_at'),
        'image': lambda x: x._single(Image, 'image'),
        'kernel': lambda x: x._single(Kernel, 'kernel'),
        'kernels': lambda x: x._multi('/droplets/%d/kernels' % x.id, Kernel, 'kernels'),
        'region': lambda x: x._single(Region, 'region'),
        'size': lambda x: x._single(Size, 'size'),
        'snapshots': lambda x: x._multi('/droplets/%d/snapshots' % x.id, Snapshot, 'snapshots'),
    }


class Image(Object):

    _SPECIAL = {
        'actions': lambda x: x._multi('/images/%d/actions' % x.id, Action, 'actions'),
        'created_at': lambda x: x._date('created_at'),
        'regions': lambda x: x._filter('/regions', Region, 'regions', lambda y: y.slug in x._data['regions']),
    }


class Kernel(Object):

    pass


class Region(Object):

    _SPECIAL = {
        'sizes': lambda x: x._filter('/sizes', Size, 'sizes', lambda y: y.slug in x._data['sizes']),
    }


class Size(Object):

    _SPECIAL = {
        'regions': lambda x: x._filter('/regions', Region, 'regions', lambda y: y.slug in x._data['regions']),
    }


class Snapshot(Object):

    pass


class SSHKey(Object):

    pass
