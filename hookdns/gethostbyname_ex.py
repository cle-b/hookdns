# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class patch_gethostbyname_ex(ContextDecorator):
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
    """
    
    def __init__(self, hosts):
        self.real_socket_gethostbyname_ex = socket.gethostbyname_ex
        self.hosts = hosts

    def _patch_socket_gethostbyname_ex(self, hostname):
        new_host = self.hosts.get(hostname, hostname)
        (_, _, ipaddrlist)  = self.real_socket_gethostbyname_ex(new_host)
        # we modify the return value with the original hostname
        # and set an empty aliaslist
        return (hostname, [], ipaddrlist) 

    def __enter__(self):
        self.mock_gethostbyname_ex = patch('socket.gethostbyname_ex') 
        mock_gethostbyname_ex2 = self.mock_gethostbyname_ex.start()
        mock_gethostbyname_ex2.side_effect = self._patch_socket_gethostbyname_ex
        return self

    def __exit__(self, *exc):
        self.mock_gethostbyname_ex.stop()
        return False
