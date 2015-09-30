#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="django-selenium-clean",
    version="0.2.0",
    license="GPL3",
    description="Write clean Selenium tests in Django",
    author="Antonis Christofides",
    author_email="anthony@itia.ntua.gr",
    url="https://github.com/aptiko/django-selenium-clean",
    packages=find_packages(),
    install_requires=[
        'django>=1.7',
        'selenium>=2.40',
    ],
)
