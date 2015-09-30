from __future__ import absolute_import

import atexit
from importlib import import_module
import os
import time

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumWrapper(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SeleniumWrapper, cls).__new__(cls, *args,
                                                                **kwargs)
        return cls._instance

    def __init__(self):
        self.driver = False
        SELENIUM_WEBDRIVERS = getattr(settings, 'SELENIUM_WEBDRIVERS', {})
        if not SELENIUM_WEBDRIVERS:
            return
        driver_id = os.environ.get('SELENIUM_WEBDRIVER', 'default')
        driver = SELENIUM_WEBDRIVERS[driver_id]
        callable = driver['callable']
        args = driver['args']
        kwargs = driver['kwargs']
        self.driver = callable(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.driver, name)

    def __setattr__(self, name, value):
        if name == 'driver':
            self.__dict__[name] = value
        else:
            setattr(self.driver, name, value)

    def __nonzero__(self):
        return bool(self.driver)

    def login(self, **credentials):
        """
        Sets selenium to appear as if a user has successfully signed in.

        Returns True if signin is possible; False if the provided
        credentials are incorrect, or the user is inactive, or if the
        sessions framework is not available.

        The code is based on django.test.client.Client.login.
        """
        user = authenticate(**credentials)
        if not (user and user.is_active
                and 'django.contrib.sessions' in settings.INSTALLED_APPS):
            return False

        engine = import_module(settings.SESSION_ENGINE)

        # Create a fake request to store login details.
        request = HttpRequest()
        request.session = engine.SessionStore()
        login(request, user)

        # Save the session values.
        request.session.save()

        # Set the cookie to represent the session.
        cookie_data = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': request.session.session_key,
            'max-age': None,
            'path': '/',
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }
        self.add_cookie(cookie_data)

        # If the cookie doesn't have a proper domain, it means selenium hadn't
        # previously connected to the site; so get the home page and re-add the
        # cookie.
        if not self.get_cookie(settings.SESSION_COOKIE_NAME)['domain']:
            self.get(self.live_server_url)
            self.add_cookie(cookie_data)

        return True

    def logout(self):
        """
        Removes the authenticated user's cookies and session object.

        Causes the authenticated user to be logged out.
        """
        session = import_module(settings.SESSION_ENGINE).SessionStore()
        session_cookie = self.get_cookie(settings.SESSION_COOKIE_NAME)
        if session_cookie:
            session.delete(session_key=session_cookie['value'])
            self.delete_cookie(settings.SESSION_COOKIE_NAME)

    def wait_until_n_windows(self, n, timeout=2):
        for i in range(timeout * 10):
            if len(self.window_handles) == n:
                return
            time.sleep(0.1)
        raise AssertionError('Timeout while waiting for {0} windows'.format(n))


selenium = SeleniumWrapper()
if selenium:
    atexit.register(lambda: selenium.driver.quit())


class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        super(SeleniumTestCase, cls).setUpClass()

        # Normally we would just do something like
        #     selenium.live_server_url = self.live_server_url
        # However, there is no "self" at this time, so we
        # essentially duplicate the code from the definition of
        # the LiveServerTestCase.live_server_url property.
        selenium.live_server_url = 'http://%s:%s' % (
            cls.server_thread.host, cls.server_thread.port)

    def __call__(self, result=None):
        if not selenium:
            return super(SeleniumTestCase, self).__call__(result)
        for width in getattr(settings, 'SELENIUM_WIDTHS', [1024]):
            selenium.set_window_size(width, 1024)
            super(SeleniumTestCase, self).__call__(result)


class PageElement(object):

    def __init__(self, *args):
        if len(args) == 2:
            self.locator = args

    def wait_until_exists(self, timeout=10):
        WebDriverWait(selenium, timeout).until(
            EC.presence_of_element_located(self.locator))

    def wait_until_not_exists(self, timeout=10):
        WebDriverWait(selenium, timeout).until_not(
            EC.presence_of_element_located(self.locator))

    def wait_until_is_displayed(self, timeout=10):
        WebDriverWait(selenium, timeout).until(
            EC.visibility_of_element_located(self.locator))

    def wait_until_not_displayed(self, timeout=10):
        WebDriverWait(selenium, timeout).until_not(
            EC.visibility_of_element_located(self.locator))

    def wait_until_contains(self, text, timeout=10):
        WebDriverWait(selenium, timeout).until(
            EC.text_to_be_present_in_element(self.locator, text))

    def wait_until_not_contains(self, text, timeout=10):
        WebDriverWait(selenium, timeout).until_not(
            EC.text_to_be_present_in_element(self.locator, text))

    def exists(self):
        return len(selenium.find_elements(*self.locator)) > 0

    def __getattr__(self, name):
        return getattr(selenium.find_element(*self.locator), name)
