# -*- coding: utf-8 -*-

import socket

from hookdns import hosts


# tests for the patch as a decorator


@hosts({"localhost": "1.2.3.4"}, only=["gethostbyname"])
def test_patch_decorator_only_gethostbyname():
    assert socket.gethostbyname("localhost") == "1.2.3.4"
    (hostname, _, ipaddrlist) = socket.gethostbyname_ex("localhost")
    assert hostname == "localhost"
    assert "127.0.0.1" in ipaddrlist
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


@hosts({"localhost": "1.2.3.4"}, only=["gethostbyname_ex"])
def test_patch_decorator_only_gethostbyname_ex():
    assert socket.gethostbyname("localhost") == "127.0.0.1"
    assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


@hosts({"localhost": "1.2.3.4"}, only=["getaddrinfo"])
def test_patch_decorator_only_getaddrinfo():
    assert socket.gethostbyname("localhost") == "127.0.0.1"
    (hostname, _, ipaddrlist) = socket.gethostbyname_ex("localhost")
    assert hostname == "localhost"
    assert "127.0.0.1" in ipaddrlist
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("1.2.3.4", 80)


@hosts({"localhost": "1.2.3.4"}, only=["gethostbyname", "gethostbyname_ex"])
def test_patch_decorator_only_gethostbyname_and_gethostbyname_ex():
    assert socket.gethostbyname("localhost") == "1.2.3.4"
    assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


# tests for the patch as a context manager


def test_patch_contextmanager_only_gethostbyname():
    with hosts({"localhost": "1.2.3.4"}, only=["gethostbyname"]):
        assert socket.gethostbyname("localhost") == "1.2.3.4"
        (hostname, _, ipaddrlist) = socket.gethostbyname_ex("localhost")
        assert hostname == "localhost"
        assert "127.0.0.1" in ipaddrlist
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("127.0.0.1", 80)


def test_patch_contextmanager_only_gethostbyname_ex():
    with hosts({"localhost": "1.2.3.4"}, only=["gethostbyname_ex"]):
        assert socket.gethostbyname("localhost") == "127.0.0.1"
        assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("127.0.0.1", 80)


def test_patch_contextmanager_only_getaddrinfo():
    with hosts({"localhost": "1.2.3.4"}, only=["getaddrinfo"]):
        assert socket.gethostbyname("localhost") == "127.0.0.1"
        (hostname, _, ipaddrlist) = socket.gethostbyname_ex("localhost")
        assert hostname == "localhost"
        assert "127.0.0.1" in ipaddrlist
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("1.2.3.4", 80)


def test_patch_contextmanager_only_gethostbyname_and_gethostbyname_ex():
    with hosts({"localhost": "1.2.3.4"}, only=["gethostbyname", "gethostbyname_ex"]):
        assert socket.gethostbyname("localhost") == "1.2.3.4"
        assert socket.gethostbyname_ex("localhost") == ("localhost", [], ["1.2.3.4"])
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("127.0.0.1", 80)
