from .account import Account
from .request import Request

_AUTH_DOMAIN = 'cloud.digitalocean.com'

READ = 'read'
WRITE = 'read write'


def begin(client_id, redirect_uri, scope=READ):
    """
    Begin the authorization code flow.

    This method will return the URL that the client should be redirected to.
    :param client_id: the client ID for the application
    :param redirect_uri: the URI to redirect the user to after completion
    :param scope: the level of access requested
    :return: the authorization URL
    """
    return Request.build_url(_AUTH_DOMAIN, '/v1/oauth/authorize', {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
    })


def complete(client_id, client_secret, redirect_uri, code):
    """
    Complete the authorization code flow.

    This method requests an access token using the provided authorization
    code and returns an Account instance if successful.
    :param client_id: the client ID for the application
    :param client_secret: the client secret for the application
    :param redirect_uri: the URI to redirect the user to after completion
    :param code: the authorization code received from the API
    :return: an Account instance if successful or None
    """
    access_token = Request.build_url(_AUTH_DOMAIN, '/v1/oauth/token', {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    })
    return Account(access_token) if access_token else None
