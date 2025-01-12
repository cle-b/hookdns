# -*- coding: utf-8 -*-
import contextlib
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple
from typing import Union
import socket


@contextlib.contextmanager
def patch_getaddrinfo(hosts: Dict[str, str]) -> Generator[None, None, None]:
    """Intercepts the call to socket.getaddrinfo to customize the DNS resolution.

    Custom DNS resolutions are describe by a dictionnary where the keys are hostnames
    and the values the expected corresponding addresses.

        {
            "hostname1": "addr1",
            "hostname2": "addr2"
        }

    hostname and addr could be a domain name or a string representation of an IPv4/IPV6.

    A call to socket.getaddrinfo for hostname1 returns the same call but for addr1.

    You can use it as a decorator or a context manager:

        @patch_getaddrinfo({"servername": "1.2.3.4"})
        def my_func():
            ...
            r = socket.getaddrinfo("servername",
                                   80,
                                   family=socket.AF_INET,
                                   proto=socket.IPPROTO_TCP)
            for (_, _, _, _, sockaddr) in r:
                assert sockaddr == ("1.2.3.4", 80)
            ...

        with patch_getaddrinfo({"servername": "1.2.3.4"}):
            ...
            r = socket.getaddrinfo("servername",
                                   80,
                                   family=socket.AF_INET,
                                   proto=socket.IPPROTO_TCP)
            for (_, _, _, _, sockaddr) in r:
                assert sockaddr == ("1.2.3.4", 80)
            ...
    https://docs.python.org/3/library/socket.html#socket.getaddrinfo
    """
    try:
        real_socket_getaddrinfo = socket.getaddrinfo

        def _patch_socket_getaddrinfo(
            host: Union[bytes, str, None],
            port: Union[bytes, str, int, None],
            family: int = 0,
            type: int = 0,
            proto: int = 0,
            flags: int = 0,
        ) -> List[
            Tuple[
                socket.AddressFamily,
                socket.SocketKind,
                int,
                str,
                Union[Tuple[str, int], Tuple[str, int, int, int]],
            ]
        ]:
            new_host = hosts.get(str(host), host) if host else host
            return real_socket_getaddrinfo(new_host, port, family, type, proto, flags)

        socket.getaddrinfo = _patch_socket_getaddrinfo

        yield
    finally:
        socket.getaddrinfo = real_socket_getaddrinfo
