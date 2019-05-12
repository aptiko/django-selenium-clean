from __future__ import absolute_import

from importlib import import_module
import os
import signal
import time

from django.conf import settings
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
            super(SeleniumWrapper, self).__setattr__(name, value)
        else:
            setattr(self.driver, name, value)

    def __bool__(self):
        return bool(self.driver)

    __nonzero__ = __bool__  # Python 2 compatibility

    def login(self, **credentials):
        """
        Sets selenium to appear as if a user has successfully signed in.

        Returns True if signin is possible; False if the provided
        credentials are incorrect, or the user is inactive, or if the
        sessions framework is not available.

        The code is based on django.test.client.Client.login.
        """
        from django.contrib.auth import authenticate, login

        # Visit the home page to ensure the cookie gets the proper domain
        self.get(self.live_server_url)

        user = authenticate(**credentials)
        if not (user and user.is_active and
                'django.contrib.sessions' in settings.INSTALLED_APPS):
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

    def quit(self):
        # The way to exit the browser is selenium.driver.quit(), however we
        # exit PhantomJS differently because of
        # https://github.com/SeleniumHQ/selenium/issues/767
        if self.driver.capabilities['browserName'] == 'phantomjs':
            self.driver.service.process.send_signal(signal.SIGTERM)
        else:
            self.driver.quit()


class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        super(SeleniumTestCase, cls).setUpClass()
        cls.selenium = SeleniumWrapper()
        PageElement.selenium = cls.selenium

        # Normally we would just do something like
        #     selenium.live_server_url = self.live_server_url
        # However, there is no "self" at this time, so we
        # essentially duplicate the code from the definition of
        # the LiveServerTestCase.live_server_url property.
        cls.selenium.live_server_url = 'http://%s:%s' % (
            cls.server_thread.host, cls.server_thread.port)

    @classmethod
    def tearDownClass(cls):

        cls.selenium.quit()
        PageElement.selenium = None
        super(SeleniumTestCase, cls).tearDownClass()

    def __call__(self, result=None):
        if hasattr(self, 'selenium'):
            for width in getattr(settings, 'SELENIUM_WIDTHS', [1024]):
                self.selenium.set_window_size(width, 1024)
        return super(SeleniumTestCase, self).__call__(result)


class PageElement(object):

    selenium = None

    def __init__(self, *args):
        if len(args) == 2:
            self.locator = args

    def wait_until_exists(self, timeout=10):
        WebDriverWait(self.selenium, timeout).until(
            EC.presence_of_element_located(self.locator))

    def wait_until_not_exists(self, timeout=10):
        WebDriverWait(self.selenium, timeout).until_not(
            EC.presence_of_element_located(self.locator))

    def wait_until_is_displayed(self, timeout=10):
        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located(self.locator))

    def wait_until_not_displayed(self, timeout=10):
        WebDriverWait(self.selenium, timeout).until_not(
            EC.visibility_of_element_located(self.locator))

    def wait_until_contains(self, text, timeout=10):
        WebDriverWait(self.selenium, timeout).until(
            EC.text_to_be_present_in_element(self.locator, text))

    def wait_until_not_contains(self, text, timeout=10):
        WebDriverWait(self.selenium, timeout).until_not(
            EC.text_to_be_present_in_element(self.locator, text))

    def wait_until_is_clickable(self, timeout=10):
        WebDriverWait(self.selenium, timeout).until(
            EC.element_to_be_clickable(self.locator))

    def exists(self):
        return len(self.selenium.find_elements(*self.locator)) > 0

    def __getattr__(self, name):
        return getattr(self.selenium.find_element(*self.locator), name)
