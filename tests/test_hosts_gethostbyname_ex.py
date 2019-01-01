# -*- coding: utf-8 -*-

import socket

import pytest

from hookdns import hosts

# tests for the real gethostbyname_ex 
def test_real_gethostbyname_ex_with_name():
    assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["127.0.0.1"])

def test_real_gethostbyname_ex_with_ip():
    assert socket.gethostbyname_ex("127.0.0.1") == ("127.0.0.1", [], ["127.0.0.1"])

def test_real_gethostbyname_ex_with_public_fqdn():
    (hostname, _, ipaddrlist) = socket.gethostbyname_ex("example.org")
    assert hostname == "example.org"
    assert len(ipaddrlist) > 0
    for ipaddr in ipaddrlist:
        assert ipaddr != "127.0.0.1"

def test_real_gethostbyname_ex_with_unknown_hostname():
    with pytest.raises((socket.herror,socket.gaierror)):
        socket.gethostbyname_ex("UNKNOWN_HOST_AZ")

# tests for the patch as a decorator

@hosts({"localhost": "1.2.3.4"})
def test_patch_decorator_with_name():
    assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])

@hosts({"127.0.0.1": "1.2.3.4"})
def test_patch_decorator_with_ip():
    assert socket.gethostbyname_ex("127.0.0.1") == ("127.0.0.1", [], ["1.2.3.4"])

@hosts({"python.org": "1.2.3.4"})
def test_patch_decorator_with_public_fqdn():
    assert socket.gethostbyname_ex("python.org") == ("python.org", [], ["1.2.3.4"])

@hosts({"python.org": "localhost"})
def test_patch_decorator_with_public_fqdn_and_a_name_for_addr():
    assert socket.gethostbyname_ex("python.org") == ("python.org", [], ["127.0.0.1"])

@hosts({"UNKNOWN_HOST_AZ": "127.0.0.1"})
def test_patch_decorator_with_unknown_hostname():
    assert socket.gethostbyname_ex("UNKNOWN_HOST_AZ") == ("UNKNOWN_HOST_AZ", [], ["127.0.0.1"])

# tests for the patch as a context manager

def test_patch_contextmanager_with_name():
    with hosts({"localhost":"1.2.3.4"}):
        assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])

def test_patch_contextmanager_with_ip():
    with hosts({"127.0.0.1":"1.2.3.4"}):
        assert socket.gethostbyname_ex("127.0.0.1") == ("127.0.0.1", [], ["1.2.3.4"])

def test_patch_contextmanager_with_public_fqdn():
    with hosts({"python.org":"1.2.3.4"}):
        assert socket.gethostbyname_ex("python.org") == ("python.org", [], ["1.2.3.4"])

def test_patch_contextmanager_with_public_fqdn_and_a_name_for_addr():
    with hosts({"python.org":"localhost"}):
        assert socket.gethostbyname_ex("python.org") == ("python.org", [], ["127.0.0.1"])

def test_patch_contextmanager_with_unknown_hostname():
    with hosts({"UNKNOWN_HOST_AZ": "127.0.0.1"}):
        assert socket.gethostbyname_ex("UNKNOWN_HOST_AZ") == ("UNKNOWN_HOST_AZ", [], ["127.0.0.1"])
