# -*- coding: utf-8 -*-

from contextlib import ContextDecorator
import socket

from mock import patch

class fake_gethostbyname(ContextDecorator):
    
    def __init__(self, hosts):
        self.real_socket_gethostbyname = socket.gethostbyname
        self.hosts = hosts

    def _fake_socket_gethostbyname(self, hostname):
        new_host = self.hosts.get(hostname, hostname)
        return self.real_socket_gethostbyname(new_host)

    def __enter__(self):
        self.mock_gethostbyname = patch('socket.gethostbyname') 
        mock_gethostbyname2 = self.mock_gethostbyname.start()
        mock_gethostbyname2.side_effect = self._fake_socket_gethostbyname
        return self

    def __exit__(self, *exc):
        self.mock_gethostbyname.stop()
        return False
