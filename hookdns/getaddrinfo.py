from collections.abc import Generator
import contextlib
import socket


@contextlib.contextmanager
def patch_getaddrinfo(hosts: dict[str, str]) -> Generator[None, None, None]:
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

        def _patch_socket_getaddrinfo(  # type: ignore[no-untyped-def]
            host,
            port,
            family=0,
            type=0,
            proto=0,
            flags=0,
        ):
            new_host = hosts.get(str(host), host) if host else host
            return real_socket_getaddrinfo(new_host, port, family, type, proto, flags)

        socket.getaddrinfo = _patch_socket_getaddrinfo

        yield
    finally:
        socket.getaddrinfo = real_socket_getaddrinfo
