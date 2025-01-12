# -*- coding: utf-8 -*-
import contextlib
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple

import socket


@contextlib.contextmanager
def patch_gethostbyname_ex(hosts: Dict[str, str]) -> Generator[None, None, None]:
    """Intercepts the call to socket.gethostbyname_ex to customize the DNS resolution.

    Custom DNS resolutions are describe by a dictionnary where the keys are hostnames
    and the values the expected corresponding addresses.

        {
            "hostname1": "addr1",
            "hostname2": "addr2"
        }

    hostname and addr could be a domain name or a string representation of an IPv4.

    A call to socket.gethostbyname_ex for hostname1 returns the same call but for addr1.

    You can use it as a decorator or a context manager:

        @patch_gethostbyname_ex({"servername": "1.2.3.4"})
        def my_func():
            ...
            assert ("servername", [], ["1.2.3.4"]) == socket.gethostbyname_ex("servername")
            ...

        with patch_gethostbyname_ex({"servername": "1.2.3.4"}):
            ...
            assert ("servername", [], ["1.2.3.4"]) == socket.gethostbyname_ex("servername")
            ...
    https://docs.python.org/3/library/socket.html#socket.gethostbyname_ex
    """  # noqa: E501
    try:
        real_socket_gethostbyname_ex = socket.gethostbyname_ex

        def _patch_socket_gethostbyname_ex(
            hostname: str,
        ) -> Tuple[str, List[str], List[str]]:
            new_host = hosts.get(hostname, hostname)
            (_, _, ipaddrlist) = real_socket_gethostbyname_ex(new_host)
            # we modify the return value with the original hostname
            # and set an empty aliaslist
            return (hostname, [], ipaddrlist)

        socket.gethostbyname_ex = _patch_socket_gethostbyname_ex

        yield
    finally:
        socket.gethostbyname_ex = real_socket_gethostbyname_ex
