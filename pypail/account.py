class Account(object):
    """
    A Digital Ocean Account.
    """

    def __init__(self, access_token):
        """
        Initialize the account with the specified access token.

        :param access_token: the access token for the account
        """
        self._access_token = access_token
