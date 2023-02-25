# -*- coding: utf-8 -*-

import socket

import pytest

from hookdns.getaddrinfo import patch_getaddrinfo


# tests for the real getaddrinfo


def test_real_getaddrinfo_with_name_ipv4():
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


def test_real_getaddrinfo_with_name_ipv6():
    r = socket.getaddrinfo(
        "ip6-localhost", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("::1", 80, 0, 0)


def test_real_getaddrinfo_with_ipv4():
    r = socket.getaddrinfo(
        "127.0.0.1", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


def test_real_getaddrinfo_with_ipv6():
    r = socket.getaddrinfo("::1", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP)
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("::1", 80, 0, 0)


def test_real_getaddrinfo_with_public_fqdn_ipv4():
    r = socket.getaddrinfo(
        "example.org", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, (ipaddr, _) in r:
        assert ipaddr != "127.0.0.1"


def test_real_getaddrinfo_with_public_fqdn_ipv6():
    r = socket.getaddrinfo(
        "example.org", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, (ipaddr, _, _, _) in r:
        assert ipaddr != "::1"


def test_real_getaddrinfo_with_unknown_hostname():
    with pytest.raises((socket.herror, socket.gaierror)):
        socket.getaddrinfo("UNKNOWN_HOST_AZ", 80)


# tests for the patch as a decorator


@patch_getaddrinfo({"localhost": "1.2.3.4"})
def test_patch_decorator_with_name_ipv4():
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("1.2.3.4", 80)


@patch_getaddrinfo({"ip6-localhost": "1::23"})
def test_patch_decorator_with_name_ipv6():
    r = socket.getaddrinfo(
        "ip6-localhost", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("1::23", 80, 0, 0)


@patch_getaddrinfo({"127.0.0.1": "1.2.3.4"})
def test_patch_decorator_with_ip_ipv4():
    r = socket.getaddrinfo(
        "127.0.0.1", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("1.2.3.4", 80)


@patch_getaddrinfo({"::1": "1::23"})
def test_patch_decorator_with_ip_ipv6():
    r = socket.getaddrinfo("::1", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP)
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("1::23", 80, 0, 0)


@patch_getaddrinfo({"example.org": "127.0.0.1"})
def test_patch_decorator_with_public_fqdn_ipv4():
    r = socket.getaddrinfo(
        "example.org", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


@patch_getaddrinfo({"example.org": "::1"})
def test_patch_decorator_with_public_fqdn_ipv6():
    r = socket.getaddrinfo(
        "example.org", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("::1", 80, 0, 0)


@patch_getaddrinfo({"example.org": "localhost"})
def test_patch_decorator_with_public_fqdn_and_a_name_for_addr():
    assert socket.getaddrinfo("example.org", 80) == socket.getaddrinfo("localhost", 80)


@patch_getaddrinfo({"example.org": "localhost"})
def test_patch_decorator_with_public_fqdn_and_a_name_for_addr_ipv4():
    family = socket.AF_INET
    assert socket.getaddrinfo("example.org", 80, family=family) == socket.getaddrinfo(
        "localhost", 80, family=family
    )


@patch_getaddrinfo({"example.org": "ip6-localhost"})
def test_patch_decorator_with_public_fqdn_and_a_name_for_addr_ipv6():
    family = socket.AF_INET6
    assert socket.getaddrinfo("example.org", 80, family=family) == socket.getaddrinfo(
        "ip6-localhost", 80, family=family
    )


@patch_getaddrinfo({"UNKNOWN_HOST_AZ": "127.0.0.1"})
def test_patch_decorator_with_unknown_hostname():
    assert socket.getaddrinfo("UNKNOWN_HOST_AZ", 80) == socket.getaddrinfo(
        "127.0.0.1", 80
    )


@patch_getaddrinfo({"localhost2": "1.2.3.4"})
def test_patch_decorator_with_another_hostname_ipv4():
    r = socket.getaddrinfo(
        "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("127.0.0.1", 80)


@patch_getaddrinfo({"localhost2": "1.2.3.4"})
def test_patch_decorator_with_another_hostname_ipv6():
    r = socket.getaddrinfo(
        "ip6-localhost", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
    )
    for _, _, _, _, sockaddr in r:
        assert sockaddr == ("::1", 80, 0, 0)


# tests for the patch as a context manager


def test_patch_contextmanager_with_name_ipv4():
    with patch_getaddrinfo({"localhost": "1.2.3.4"}):
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("1.2.3.4", 80)


def test_patch_contextmanager_with_name_ipv6():
    with patch_getaddrinfo({"ip6-localhost": "1::23"}):
        r = socket.getaddrinfo(
            "ip6-localhost", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("1::23", 80, 0, 0)


def test_patch_contextmanager_with_ip_ipv4():
    with patch_getaddrinfo({"127.0.0.1": "1.2.3.4"}):
        r = socket.getaddrinfo(
            "127.0.0.1", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("1.2.3.4", 80)


def test_patch_contextmanager_with_ip_ipv6():
    with patch_getaddrinfo({"::1": "1::23"}):
        r = socket.getaddrinfo(
            "::1", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("1::23", 80, 0, 0)


def test_patch_contextmanager_with_public_fqdn_ipv4():
    with patch_getaddrinfo({"example.org": "127.0.0.1"}):
        r = socket.getaddrinfo(
            "example.org", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("127.0.0.1", 80)


def test_patch_contextmanager_with_public_fqdn_ipv6():
    with patch_getaddrinfo({"example.org": "::1"}):
        r = socket.getaddrinfo(
            "example.org", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("::1", 80, 0, 0)


def test_patch_contextmanager_with_public_fqdn_and_a_name_for_addr():
    with patch_getaddrinfo({"example.org": "localhost"}):
        assert socket.getaddrinfo("example.org", 80) == socket.getaddrinfo(
            "localhost", 80
        )


def test_patch_contextmanager_with_public_fqdn_and_a_name_for_addr_ipv4():
    with patch_getaddrinfo({"example.org": "localhost"}):
        family = socket.AF_INET
        assert socket.getaddrinfo(
            "example.org", 80, family=family
        ) == socket.getaddrinfo("localhost", 80, family=family)


def test_patch_contextmanager_with_public_fqdn_and_a_name_for_addr_ipv6():
    with patch_getaddrinfo({"example.org": "ip6-localhost"}):
        family = socket.AF_INET6
        assert socket.getaddrinfo(
            "example.org", 80, family=family
        ) == socket.getaddrinfo("ip6-localhost", 80, family=family)


def test_patch_contextmanager_with_unknown_hostname():
    with patch_getaddrinfo({"UNKNOWN_HOST_AZ": "127.0.0.1"}):
        assert socket.getaddrinfo("UNKNOWN_HOST_AZ", 80) == socket.getaddrinfo(
            "127.0.0.1", 80
        )


def test_patch_contextmanager_with_another_hostname_ipv4():
    with patch_getaddrinfo({"localhost2": "1.2.3.4"}):
        r = socket.getaddrinfo(
            "localhost", 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("127.0.0.1", 80)


def test_patch_contextmanager_with_another_hostname_ipv6():
    with patch_getaddrinfo({"localhost2": "1.2.3.4"}):
        r = socket.getaddrinfo(
            "ip6-localhost", 80, family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        for _, _, _, _, sockaddr in r:
            assert sockaddr == ("::1", 80, 0, 0)
