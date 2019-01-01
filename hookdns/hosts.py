# -*- coding: utf-8 -*-

from contextlib import ContextDecorator, ExitStack

from .getaddrinfo import patch_getaddrinfo
from .gethostbyname import patch_gethostbyname
from .gethostbyname_ex import patch_gethostbyname_ex

class hosts(ContextDecorator):

    def __init__(self, hosts, only=None):
        self.hosts = hosts
        if only is None:
            self.patchs = ["gethostbyname", "gethostbyname_ex", "getaddrinfo"]
        else:
            self.patchs = only
        self.exit_stack = ExitStack()

    def __enter__(self):
        if "gethostbyname" in self.patchs:
            self.exit_stack.enter_context(patch_gethostbyname(self.hosts))
        if "gethostbyname_ex" in self.patchs:
            self.exit_stack.enter_context(patch_gethostbyname_ex(self.hosts))
        if "getaddrinfo" in self.patchs:
            self.exit_stack.enter_context(patch_getaddrinfo(self.hosts))
        return self

    def __exit__(self, *exc):
        self.exit_stack.close()
        return False
