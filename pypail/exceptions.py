class APIError(Exception):
    """
    An error encountered while attempting to access the Digital Ocean API.

    The APIError exception is a base for all other exceptions raised by pypail.
    """


class ConnectionError(APIError):
    """
    An error encountered while trying to establish a connection to the API.
    """

    def __init__(self):
        super(ConnectionError, self).__init__('unable to establish a connection to the API')


class MalformedResponseError(APIError):
    """
    An error encountered while parsing the API response.
    """

    def __init__(self):
        super(MalformedResponseError, self).__init__('unable to parse API response')
