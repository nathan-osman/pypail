## pypail - Python Digital Ocean Client

pypail is a lightweight Python package that simplifies access to the Digital Ocean API.

### Installation

[TODO]

### Authentication

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

    credentials = auth.complete(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://example.org',
        code=CODE,
    )

If all went well, credentials will be an instance of the Credentials class, which is used by all of the other classes to make requests. The credentials class does not persist the values to disk, so you will need to take care of that if you plan to use the credentials beyond the lifetime of the current script. This can be done by storing a copy of the data attribute:

    f = open('credentials.json', 'w')
    f.write(json.dumps(credentials.data))
    f.close()

To load the credentials later, simply reverse the process:

    f = open('credentials.json', 'r')
    credentials = Credentials(json.loads(f.read()))
    f.close()

### Making Requests

Once you have valid credentials, you will need to create an instance of the Account class in order to begin making requests:

    from pypail import objects
    account = objects.Account(credentials)

To obtain a list of all droplets in an account, simple enumerate the droplets property of the account:

    for droplet in account.droplets:
        print droplet.name
