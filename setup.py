#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
    ],
    name="django-selenium-clean",
    version="0.3.1",
    license="BSD 3-Clause License",
    description="Write clean Selenium tests in Django",
    author="Antonis Christofides",
    author_email="antonis@djangodeployment.com",
    url="https://github.com/aptiko/django-selenium-clean",
    packages=find_packages(),
    install_requires=[
        'django>=1.11,<3',
        'selenium>=2.40,<4',
    ],
    test_suite="tests.tests",
)
