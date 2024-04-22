#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
    ],
    name="django-selenium-clean",
    version="0.0.1.dev0",
    license="BSD 3-Clause License",
    description="Write clean Selenium tests in Django",
    author="Antonis Christofides",
    author_email="antonis@djangodeployment.com",
    url="https://github.com/aptiko/django-selenium-clean",
    packages=find_packages(),
    install_requires=["django>=2.2,<6", "selenium>=3,<5"],
    test_suite="tests.tests",
)
