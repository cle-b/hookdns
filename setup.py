# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    desc = fh.read()
    long_description = desc[desc.find("# hookdns"):] # remove bagde

setuptools.setup(
    name="hookdns",
    version="1.0.0",
    author="cle-b",
    author_email="cle@tictac.pm",
    description="An easy way to customize the dns resolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cle-b/hookdns",
    packages=setuptools.find_packages(),
    python_requires=">=3.4",
    install_requires=[
          'mock',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
)