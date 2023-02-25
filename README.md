[![Build Status](https://github.com/cle-b/hookdns/workflows/Build/badge.svg?branch=main)](https://github.com/cle-b/hookdns/actions?query=workflow%3ABuild) [![Coverage Status](https://coveralls.io/repos/github/cle-b/hookdns/badge.svg?branch=main)](https://coveralls.io/github/cle-b/hookdns?branch=main) [![PyPI version](https://badge.fury.io/py/hookdns.svg)](https://pypi.org/project/hookdns/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

# hookdns

HookDNS is a library which allow you to modify a name resolution in your Python script without any modification in your hosts file or by using a fake DNS resolver.

## Installation

```
pip install hookdns
```

## Usage

Custom DNS resolutions are describe by a dictionnary where the keys are hostnames
and the values the expected corresponding addresses.    

    {
        "hostname1": "addr1",
        "hostname2": "addr2"
    }

hostname and addr could be a domain name or a string representation of an IPv4/IPV6.

### Example using the patch as a decorator

```python
import requests

from hookdns import hosts

@hosts({"example.org": "localhost"})
def myfunc():
    ...
    r = requests.get("http://example.org") # the request is sent to your local server
    ...
```

### Example using the patch as a context manager

```python
import requests

from hookdns import hosts

with hosts({"example.org": "localhost"}):
    ...
    r = requests.get("http://example.org") # the request is sent to your local server
    ...
```
### Options

By default the following function calls are intercepted: *socket.gethostbyname, socket.gethostbyname_ex and socket.getaddrinfo*.

You can limit the interception to only a restricted list of function.

```python
import socket

from hookdns import hosts

with hosts({"example.org": "localhost"}, only=["gethostbyname"]):
    ...
    addr = socket.gethostbyname("example.org") # returns "127.0.0.1"
    print("gethostname returns: %s" % addr)

    _, _, addr = socket.gethostbyname_ex("example.org") # returns the real ip address for example.org
    print("gethostname_ex returns: %s" % addr[0])
    ...    
```
```
gethostname returns: 127.0.0.1
gethostname_ex returns: 93.184.216.34
```


## Limitation

It works only with Python 3.4 and greater.
