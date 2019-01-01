# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class patch_getaddrinfo(ContextDecorator):
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
    
    def __init__(self, hosts):
        self.real_socket_getaddrinfo = socket.getaddrinfo
        self.hosts = hosts

    def _patch_socket_getaddrinfo(self, host, port, family=0, type=0, proto=0, flags=0):
        new_host = self.hosts.get(host, host)        
        return self.real_socket_getaddrinfo(new_host, port, family, type, proto, flags)

    def __enter__(self):
        self.mock_getaddrinfo = patch('socket.getaddrinfo') 
        mock_getaddrinfo2 = self.mock_getaddrinfo.start()
        mock_getaddrinfo2.side_effect = self._patch_socket_getaddrinfo
        return self

    def __exit__(self, *exc):
        self.mock_getaddrinfo.stop()
        return False
