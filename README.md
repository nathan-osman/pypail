## pypail - Python Digital Ocean Client

[![PyPI Version](http://img.shields.io/pypi/v/pypail.svg)](https://pypi.python.org/pypi/pypail)
[![PyPI Downloads](http://img.shields.io/pypi/dm/pypail.svg)](https://pypi.python.org/pypi/pypail)
[![License](http://img.shields.io/badge/license-MIT-red.svg)](http://opensource.org/licenses/MIT)

pypail is a lightweight Python package that simplifies access to the Digital Ocean API.

### Installation

You can install pypail directly from PyPI

    pip install pypail

pypail depends on two other Python packages: [requests](https://pypi.python.org/pypi/requests) and [python-dateutil](https://pypi.python.org/pypi/python-dateutil).

### Authentication

In order to issue requests to the Digital Ocean API, you will need to [register your application](https://cloud.digitalocean.com/settings/applications/new). You will be asked to provide some information about your application, including a callback URL. Once completed, you will receive a client ID and client secret. Use those two values to begin the authorization flow:

    from pypail import auth

    CLIENT_ID = '1234567890'
    CLIENT_SECRET = 'abcdefghijklmnopqrst'

    print auth.begin(
        client_id=CLIENT_ID,
        redirect_uri='http://example.org',
        scope=auth.WRITE,
    )

This will display the authorization URL. The client will need to view this URL in their browser and authorize the application. The second parameter specifies the callback URL that you provided when registering your application. If the client authorizes your application, they will be redirected to your callback URL with a special code in the query string. Once you have the code, you can use it to obtain an access token:

    CODE =  # ...obtained from query string...

    credentials = auth.complete(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://example.org',
        code=CODE,
    )

If all went well, `credentials` will be an instance of the `Credentials` class, which is used by all of the other classes to make requests. The credentials class does not persist the values to disk, so you will need to take care of that if you plan to use the credentials beyond the lifetime of the current script. This can be done by storing a copy of the `data` attribute:

    f = open('credentials.json', 'w')
    f.write(json.dumps(credentials.data))
    f.close()

To load the credentials later, simply reverse the process:

    f = open('credentials.json', 'r')
    credentials = Credentials(json.loads(f.read()))
    f.close()

### Making Requests

Once you have valid credentials, you will need to create an instance of the `Account` class in order to begin making requests:

    from pypail import objects
    account = objects.Account(credentials)

Once you have an `Account` instance, you can use its attributes to retrieve information from the API. For example, the `droplets` attribute will return a generator for enumerating droplets in the account:

    for droplet in account.droplets:
        print droplet.name

The droplet instance contains the attributes listed [here](https://developers.digitalocean.com/v2/#droplets). Attributes that return a date are automatically converted to instances of Python's datetime class. Attributes that end in `_id` (such as `backup_ids`) can be accessed through their plural form (`backups`) to obtain the full object:

    snapshots = [s.name for s in droplet.snapshots]

In the example above, `snapshots` will contain a list of snapshot names.

### Contributing

pypail is an open source project and we welcome contributions in a number of important areas:

- **Code:** although the authorization classes and most object access methods are complete, there are a number of features planned for a future release that haven't been completed or even started yet:

    - only the first page of results are enumerated rather than multiple pages
    - objects cannot be created, modified, or deleted - access is read-only
    - there are currently no tests written

- **Documentation:** except for this document, no documentation for pypail exists, although virtually all classes and methods have correctly formatted docstrings

If any of this sounds like something you would be interested in helping with, please contact me or submit a pull request. Thanks in advance!
