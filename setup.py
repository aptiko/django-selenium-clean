#!/usr/bin/env python

import os

from setuptools import setup, find_packages
from setuptools.command.test import test


class CustomTestCommand(test):

    def run(self):
        import django
        from django.conf import settings
        from django.core import management
        from selenium import webdriver

        settings.configure(
            ROOT_URLCONF='tests.urls',
            ALLOWED_HOSTS=['*'],
            MIDDLEWARE_CLASSES=[
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
            ],
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                                   'NAME': ':memory:'}},
            STATIC_URL='/static/',
            INSTALLED_APPS=['django.contrib.contenttypes',
                            'django.contrib.auth',
                            'django.contrib.sessions',
                            ],
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(os.path.dirname(__file__), 'tests',
                                     'templates')],
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.request',
                    ],
                },
            }],
            SELENIUM_WEBDRIVERS={
                'default': {
                    'callable': webdriver.Firefox,
                    'args': (),
                    'kwargs': {},
                },
            }
        )
        django.setup()
        management.call_command('migrate')

        test.run(self)


setup(
    name="django-selenium-clean",
    version="DEV",
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
    cmdclass={'test': CustomTestCommand},
    test_suite="tests.tests",
)
