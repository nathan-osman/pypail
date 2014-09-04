## pypail - Python Digital Ocean Client

pypail is a lightweight Python package that simplifies access to the Digital Ocean API.

### Installation

[TODO]

### Usage

In order to issue requests to the Digital Ocean API, you will need to register your application. You will be asked to provide some information about your application, including a callback URL. Once completed, you will receive a client ID and client secret. Use those two values to begin the authorization flow:

    from pypail import auth

    CLIENT_ID = '1234567890'
    CLIENT_SECRET = 'abcdefghijklmnopqrst'

    print auth.begin(
        client_id=CLIENT_ID,
        redirect_uri='http://example.org',
        scope=auth.WRITE,
    )

This will display the authorization URL. The client will need to view this URL in their browser and authorize the application. The second parameter specifies the callback URL that you provided when registering your application. This callback will receive an authorization code if successful. Once you have the code, you can use it to obtain an access token:

    CODE =  # ...obtained from query string...

    account = auth.complete(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://example.org',
        code=CODE,
    )

If all went well, account will be an instance of the Account class, which provides you full access to the API.
