# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hookdns",
    version="0.0.1",
    author="cle-b",
    author_email="cle@tictac.pm",
    description="An easy way to customize the dns resolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cle-b/hookdns",
    packages=setuptools.find_packages(),
    install_requires=[
          'mock',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
)