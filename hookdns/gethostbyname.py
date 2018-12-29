# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class patch_gethostbyname(ContextDecorator):
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
    
    def __init__(self, hosts):
        self.real_socket_gethostbyname = socket.gethostbyname
        self.hosts = hosts

    def _patch_socket_gethostbyname(self, hostname):
        new_host = self.hosts.get(hostname, hostname)
        return self.real_socket_gethostbyname(new_host)

    def __enter__(self):
        self.mock_gethostbyname = patch('socket.gethostbyname') 
        mock_gethostbyname2 = self.mock_gethostbyname.start()
        mock_gethostbyname2.side_effect = self._patch_socket_gethostbyname
        return self

    def __exit__(self, *exc):
        self.mock_gethostbyname.stop()
        return False
