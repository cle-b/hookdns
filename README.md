[![Build](https://github.com/cle-b/hookdns/actions/workflows/build.yml/badge.svg)](https://github.com/cle-b/hookdns/actions/workflows/build.yml) [![Coverage Status](https://coveralls.io/repos/github/cle-b/hookdns/badge.svg?branch=main)](https://coveralls.io/github/cle-b/hookdns?branch=main) [![PyPI version](https://badge.fury.io/py/hookdns.svg)](https://pypi.org/project/hookdns/)

# hookdns

HookDNS is a library which allow you to modify a name resolution in your Python script without any modification in your hosts file or by using a fake DNS resolver.

```python
import requests

from hookdns import hosts

with hosts({"example.org": "127.0.0.1"}):
    ...
    r = requests.get("http://example.org")  # the request is sent to your local server
    ...
```

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

@hosts({"example.org": "127.0.0.1"})
def myfunc():
    ...
    r = requests.get("http://example.org")  # the request is sent to your local server
    ...
```

### Example using the patch as a context manager

```python
import requests

from hookdns import hosts

with hosts({"example.org": "localhost"}):
    ...
    r = requests.get("http://example.org")  # the request is sent to your local server
    ...
```
