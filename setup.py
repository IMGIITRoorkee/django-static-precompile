#!/usr/bin/env python
from setuptools import setup, find_packages

# setup the project
setup(
    name="django-static-precompile",
    version="0.0.1",
    author="Information Management Group",
    author_email="img.iitr.img@gmail.com",
    description="Static files precompilers for django",
    license="MIT",
    packages=find_packages(exclude=["tests", ]),
)
