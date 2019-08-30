import os
from tempfile import NamedTemporaryFile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

DEBUG = False

ROOT_URLCONF = 'tests.urls'

SECRET_KEY = 'topsecret'

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': NamedTemporaryFile().name,
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

headless = ChromeOptions()
headless.add_argument("--headless")

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.__dict__[os.environ.get('SELENIUM_BROWSER',
                                                      'Chrome')],
        'args': [],
        'kwargs': {},
    },
    "headless": {
        "callable": webdriver.Chrome, "args": [], "kwargs": {"options": headless}
    },
}
