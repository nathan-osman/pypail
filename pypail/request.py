from requests import request, Request, RequestException

from .exceptions import APIError, ConnectionError, ResponseError


def build_url(domain, path, params={}):
    """
    Build a URL from its components.

    :param domain: the domain name for the request
    :param path: the path for the request
    :param params: zero or more query string parameters
    :return: the described URL
    """
    return Request('GET', 'https://%s%s' % (domain, path), params=params).prepare().url


def send_request(method, domain, path, params={}):
    """
    Send an HTTP request.

    :param domain: the domain name for the request
    :param path: the path for the request
    :param params: zero or more query string parameters
    :return: the HTTP response or None
    """
    try:
        data = request(method, 'https://%s%s' % (domain, path), params=params).json()
    except RequestException:
        raise ConnectionError()
    except ValueError:
        raise ResponseError()
    if 'error' in data:
        raise APIError(data.get('error_description'), 'unknown API error')
    return data
