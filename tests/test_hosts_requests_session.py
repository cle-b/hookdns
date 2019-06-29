# -*- coding: utf-8 -*-

import pytest
import requests

from hookdns import hosts


def test_real_requests_with_public_fqdn():
    r = requests.Session()
    assert "Example Domain" in r.get("http://example.org/").text
    assert "Example Domain" in r.get("http://example.org/").text


def test_real_requests_name(httpd, httpdport):
    r = requests.Session()
    assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text
    assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text


def test_real_requests_ip(httpd, httpdport):
    r = requests.Session()
    assert "from 127.0.0.1" in r.get("http://127.0.0.1:%d/" % httpdport).text
    assert "from 127.0.0.1" in r.get("http://127.0.0.1:%d/" % httpdport).text


def test_real_requests_with_unknown_hostname():
    r = requests.Session()
    with pytest.raises(requests.exceptions.ConnectionError):
        r.get("http://UNKNOWN_HOST_AZ")


# during the tests, a http server is launched locally.
# the server always responds the text "from xxx" where xxx is the 'Host' header value

# tests for the patch as a decorator


@hosts({"example.org": "localhost"})
def test_patch_decorator_with_name(httpd, httpdport):
    r = requests.Session()
    assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text
    assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text


@hosts({"example.org": "127.0.0.1"})
def test_patch_decorator_with_ipv4(httpd, httpdport):
    r = requests.Session()
    assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text
    assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text


@hosts({"unknown_host_az": "127.0.0.1"})  # don't work if hostname is in upper case
def test_patch_decorator_with_unknown_hostname(httpd, httpdport):
    r = requests.Session()
    assert (
        "from unknown_host_az" in r.get("http://unknown_host_az:%d/" % httpdport).text
    )
    assert (
        "from unknown_host_az" in r.get("http://unknown_host_az:%d/" % httpdport).text
    )


@hosts({"anotherhostname": "1.2.3.4"})
def test_patch_decorator_with_another_hostname(httpd, httpdport):
    r = requests.Session()
    assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text
    assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text


# tests for the patch as a context manager


def test_patch_contextmanager_with_name(httpd, httpdport):
    r = requests.Session()
    with hosts({"example.org": "localhost"}):
        assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text
        assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text


def test_patch_contextmanager_with_ipv4(httpd, httpdport):
    r = requests.Session()
    with hosts({"example.org": "127.0.0.1"}):
        assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text
        assert "from example.org" in r.get("http://example.org:%d/" % httpdport).text


def test_patch_contextmanager_with_unknown_hostname(httpd, httpdport):
    r = requests.Session()
    # don't work if hostname is in upper case
    with hosts({"unknown_host_az": "127.0.0.1"}):
        assert (
            "from unknown_host_az"
            in r.get("http://unknown_host_az:%d/" % httpdport).text
        )
        assert (
            "from unknown_host_az"
            in r.get("http://unknown_host_az:%d/" % httpdport).text
        )


def test_patch_contextmanager_with_another_hostname(httpd, httpdport):
    r = requests.Session()
    with hosts({"anotherhostname": "1.2.3.4"}):
        assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text
        assert "from localhost" in r.get("http://localhost:%d/" % httpdport).text
