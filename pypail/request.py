from urllib import quote
from urllib2 import URLError, urlopen


class Request(object):
    """
    Methods for interacting with the Digital Ocean API.
    """

    @classmethod
    def build_url(cls, domain, path, params={}):
        """
        Build a URL from its components.

        :param domain: the domain name for the request
        :param path: the path for the request
        :param params: zero or more query string parameters
        :return: the described URL
        """
        return 'https://%s%s%s%s' % (domain, path, '?' if params else '', quote(params))

    @classmethod
    def send_request(cls, domain, path, params={}):
        """
        Send an HTTP request.

        :param domain: the domain name for the request
        :param path: the path for the request
        :param params: zero or more query string parameters
        :return: the HTTP response or None
        """
        try:
            data = urlopen(cls.build_url(domain, path, params)).read()
        except URLError:
            return None
        else:
            return data
