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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
    ],
    name="django-selenium-clean",
    version="0.2.1",
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
