# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class fake_gethostbyname_ex(ContextDecorator):
    
    def __init__(self, hosts):
        self.real_socket_gethostbyname_ex = socket.gethostbyname_ex
        self.hosts = hosts

    def _fake_socket_gethostbyname_ex(self, hostname):
        new_host = self.hosts.get(hostname, hostname)
        (_, aliaslist, ipaddrlist)  = self.real_socket_gethostbyname_ex(new_host)
        return (hostname, aliaslist, ipaddrlist)

    def __enter__(self):
        self.mock_gethostbyname_ex = patch('socket.gethostbyname_ex') 
        mock_gethostbyname_ex2 = self.mock_gethostbyname_ex.start()
        mock_gethostbyname_ex2.side_effect = self._fake_socket_gethostbyname_ex
        return self

    def __exit__(self, *exc):
        self.mock_gethostbyname_ex.stop()
        return False
