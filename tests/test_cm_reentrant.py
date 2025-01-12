# -*- coding: utf-8 -*-
import requests

from hookdns import hosts


def test_reentrant(httpd, httpdport):
    with hosts({"xyz": "localhost"}):
        with hosts({"example.org": "xyz"}):
            assert (
                "from example.org"
                in requests.get("http://example.org:%d/" % httpdport).text
            )
