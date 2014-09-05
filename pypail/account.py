class Account(object):
    """
    A Digital Ocean Account.
    """

    def __init__(self, **kwargs):
        """
        Initialize the account with the specified data.

        This method accepts data either directly returned by completing the
        authorization code flow or using a stored access token.

        :param **kwargs: authentication data retrieved from the API
        """
        self.access_token = kwargs.get('access_token', None)
        self.refresh_token = kwargs.get('refresh_token', None)
