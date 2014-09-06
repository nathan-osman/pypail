from requests import request, Request

READ = 'read'
WRITE = 'read write'


class APIError(Exception):
    """
    An error encountered while attempting to access the Digital Ocean API.
    """


def _request(*args, **kwargs):
    """
    Issue a request and return the response as JSON.
    """
    data = request(*args, **kwargs).json()
    if 'error' in data:
        raise APIError(data.get('error_description'), 'unknown API error')
    return data


class Credentials(object):
    """
    Storage for API credentials.
    """

    def __init__(self, **kwargs):
        """
        Initialize with data.

        :param **kwargs: data returned from completing authorization
        """
        self.data = kwargs

    def request(self, endpoint, method=None, **kwargs):
        """
        Issue a request to the provided endpoint.

        :param endpoint: the endpoint to use for the request
        :param method: the HTTP request method to use
        :param **kwargs: any additional parameters for request
        :return: the response as JSON
        """
        return _request(method or 'GET', 'https://api.digitalocean.com/v2%s' % endpoint, **kwargs)


def begin(client_id, redirect_uri, scope=READ):
    """
    Begin the authorization code flow.

    This method will return the URL that the client should be redirected to.

    :param client_id: the client ID for the application
    :param redirect_uri: the URI to redirect the user to after completion
    :param scope: the level of access requested
    :return: the authorization URL
    """
    return Request('GET', 'https://cloud.digitalocean.com/v1/oauth/authorize', params={
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
    }).prepare().url


def complete(client_id, client_secret, redirect_uri, code):
    """
    Complete the authorization code flow.

    This method requests an access token using the provided authorization
    code and returns a Credential instance. The authentication data can be
    retrieved from the Credential instance by accessing the data property.

    :param client_id: the client ID for the application
    :param client_secret: the client secret for the application
    :param redirect_uri: the URI to redirect the user to after completion
    :param code: the authorization code received from the API
    :return: a Credentials instance
    """
    return Credentials(**_request('POST', 'https://cloud.digitalocean.com/v1/oauth/token', params={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }))
