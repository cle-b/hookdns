# -*- coding: utf-8 -*-
import contextlib
from typing import Dict
from typing import Generator

from hookdns.getaddrinfo import patch_getaddrinfo
from hookdns.gethostbyname import patch_gethostbyname
from hookdns.gethostbyname_ex import patch_gethostbyname_ex


@contextlib.contextmanager
def hosts(hosts: Dict[str, str]) -> Generator[None, None, None]:
    """Customize DNS resolutions based on a dictionary where the keys are hostnames and the values are the corresponding expected addresses.

        {
            "hostname1": "addr1",
            "hostname2": "addr2"
        }

    Hostnames and addresses can be either a FQDN or a string representation of an IPv4/IPv6 address.

    You can use this as a decorator or a context manager:

        @hosts({"servername": "1.2.3.4"})
        def my_func():
            ...
            r = socket.getaddrinfo("servername",
                                   80,
                                   family=socket.AF_INET,
                                   proto=socket.IPPROTO_TCP)
            for (_, _, _, _, sockaddr) in r:
                assert sockaddr == ("1.2.3.4", 80)
            ...

        with hosts({"servername": "1.2.3.4"}):
            ...
            r = socket.getaddrinfo("servername",
                                   80,
                                   family=socket.AF_INET,
                                   proto=socket.IPPROTO_TCP)
            for (_, _, _, _, sockaddr) in r:
                assert sockaddr == ("1.2.3.4", 80)
            ...
    """  # noqa: E501

    with patch_gethostbyname(hosts):
        with patch_gethostbyname_ex(hosts):
            with patch_getaddrinfo(hosts):
                yield
