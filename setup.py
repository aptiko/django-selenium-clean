#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="django-selenium-clean",
    version="DEV",
    license="MIT",
    description="Write clean Selenium tests in Django",
    author="Antonis Christofides",
    author_email="antonis@djangodeployment.com",
    url="https://github.com/aptiko/django-selenium-clean",
    packages=find_packages(),
    install_requires=[
        'django>=1.8,<2',
        'selenium>=2.40,<4',
    ],
    test_suite="tests.tests",
)
