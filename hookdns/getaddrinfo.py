# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class fake_getaddrinfo(ContextDecorator):
    
    def __init__(self, hosts):
        self.real_socket_getaddrinfo = socket.getaddrinfo
        self.hosts = hosts

    def _fake_socket_getaddrinfo(self, host, port, family=0, type=0, proto=0, flags=0):
        new_host = self.hosts.get(host, host)        
        return self.real_socket_getaddrinfo(new_host, port, family, type, proto, flags)

    def __enter__(self):
        self.mock_getaddrinfo = patch('socket.getaddrinfo') 
        mock_getaddrinfo2 = self.mock_getaddrinfo.start()
        mock_getaddrinfo2.side_effect = self._fake_socket_getaddrinfo
        return self

    def __exit__(self, *exc):
        self.mock_getaddrinfo.stop()
        return False
