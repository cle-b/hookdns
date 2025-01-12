# -*- coding: utf-8 -*-
import contextlib
from typing import Dict
from typing import Generator
import socket


@contextlib.contextmanager
def patch_gethostbyname(hosts: Dict[str, str]) -> Generator[None, None, None]:
    """Intercepts the call to socket.gethostbyname to customize the DNS resolution.

    Custom DNS resolutions are describe by a dictionnary where the keys are hostnames
    and the values the expected corresponding addresses.

        {
            "hostname1": "addr1",
            "hostname2": "addr2"
        }

    hostname and addr could be a domain name or a string representation of an IPv4.

    A call to socket.gethostbyname for hostname1 returns the same call but for addr1.

    You can use it as a decorator or a context manager:

        @patch_gethostbyname({"servername": "1.2.3.4"})
        def my_func():
            ...
            assert "1.2.3.4" == socket.gethostbyname("servername")
            ...

        with patch_gethostbyname({"servername": "1.2.3.4"}):
            ...
            assert "1.2.3.4" == socket.gethostbyname("servername")
            ...
    https://docs.python.org/3/library/socket.html#socket.gethostbyname
    """

    try:
        real_socket_gethostbyname = socket.gethostbyname

        def _patch_socket_gethostbyname(hostname: str) -> str:
            new_host = hosts.get(hostname, hostname)
            return real_socket_gethostbyname(new_host)

        socket.gethostbyname = _patch_socket_gethostbyname

        yield
    finally:
        socket.gethostbyname = real_socket_gethostbyname
