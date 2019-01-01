# -*- coding: utf-8 -*-

import socket

import pytest

from hookdns import hosts

# tests for the real gethostbyname 
def test_real_gethostbyname_with_name():
    assert socket.gethostbyname("localhost") == "127.0.0.1"

def test_real_gethostbyname_with_ip():
    assert socket.gethostbyname("127.0.0.1") == "127.0.0.1"

def test_real_gethostbyname_with_public_fqdn():
    assert socket.gethostbyname("example.org") != "127.0.0.1"

def test_real_gethostbyname_with_unknown_hostname():
    with pytest.raises((socket.herror,socket.gaierror)):
        socket.gethostbyname("UNKNOWN_HOST_AZ")

# tests for the patch as a decorator

@hosts({"localhost": "1.2.3.4"})
def test_patch_decorator_with_name():
    assert socket.gethostbyname("localhost") == "1.2.3.4"

@hosts({"127.0.0.1": "1.2.3.4"})
def test_patch_decorator_with_ip():
    assert socket.gethostbyname("127.0.0.1") == "1.2.3.4"

@hosts({"example.org": "1.2.3.4"})
def test_patch_decorator_with_public_fqdn():
    assert socket.gethostbyname("example.org") == "1.2.3.4"

@hosts({"example.org": "localhost"})
def test_patch_decorator_with_public_fqdn_and_a_name_for_addr():
    assert socket.gethostbyname("example.org") == "127.0.0.1"

@hosts({"UNKNOWN_HOST_AZ": "127.0.0.1"})
def test_patch_decorator_with_unknown_hostname():
    assert socket.gethostbyname("UNKNOWN_HOST_AZ") == "127.0.0.1"

@hosts({"localhost2": "1.2.3.4"})
def test_patch_decorator_with_another_hostname():
    assert socket.gethostbyname("localhost") == "127.0.0.1"

# tests for the patch as a context manager

def test_patch_contextmanager_with_name():
    with hosts({"localhost": "1.2.3.4"}):
        assert socket.gethostbyname("localhost") == "1.2.3.4"

def test_patch_contextmanager_with_ip():
    with hosts({"127.0.0.1": "1.2.3.4"}):
        assert socket.gethostbyname("127.0.0.1") == "1.2.3.4"

def test_patch_contextmanager_with_public_fqdn():
    with hosts({"example.org": "1.2.3.4"}):
        assert socket.gethostbyname("example.org") == "1.2.3.4"

def test_patch_contextmanager_with_public_fqdn_and_a_name_for_addr():
    with hosts({"example.org": "localhost"}):
        assert socket.gethostbyname("example.org") == "127.0.0.1"

def test_patch_contextmanager_with_unknown_hostname():
    with hosts({"UNKNOWN_HOST_AZ": "127.0.0.1"}):
        assert socket.gethostbyname("UNKNOWN_HOST_AZ") == "127.0.0.1"

def test_patch_contextmanager_with_another_hostname():
    with hosts({"localhost2": "1.2.3.4"}):
        assert socket.gethostbyname("localhost") == "127.0.0.1"
