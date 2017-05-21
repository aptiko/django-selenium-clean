import os
from selenium import webdriver

DEBUG = False

ROOT_URLCONF = 'tests.urls'

SECRET_KEY = 'topsecret'

ALLOWED_HOSTS = ['*']

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

STATIC_URL = '/static/'

INSTALLED_APPS = ['django.contrib.contenttypes',
                  'django.contrib.auth',
                  'django.contrib.sessions',
                  ]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
        ],
    },
}]

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.__dict__[os.environ.get('SELENIUM_BROWSER',
                                                      'Chrome')],
        'args': (),
        'kwargs': {},
    },
}
