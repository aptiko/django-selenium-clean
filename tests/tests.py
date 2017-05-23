import os
from unittest import SkipTest

import django
from django.core import management
from django.test import override_settings, TestCase

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from django_selenium_clean import PageElement, SeleniumTestCase


class DjangoSeleniumCleanTestCase(SeleniumTestCase):

    heading_earth = PageElement(By.ID, 'earth')
    heading_world = PageElement(By.ID, 'world')
    user_info = PageElement(By.ID, 'user')
    button_toggle_heading = PageElement(By.ID, 'toggle-heading')
    button_open_window = PageElement(By.ID, 'open-window')
    button_toggle_element = PageElement(By.ID, 'toggle-element')
    button_toggle_message = PageElement(By.ID, 'toggle-message')
    togglable = PageElement(By.ID, 'togglable')
    message = PageElement(By.ID, 'message')

    def test_toggle(self):
        self.selenium.get(self.live_server_url)

        # Check that "Greetings to earth" is visible
        self.assertTrue(self.heading_earth.is_displayed())
        self.assertFalse(self.heading_world.is_displayed())

        # Toggle and check that "Hello world" is visible
        self.button_toggle_heading.click()
        self.heading_world.wait_until_is_displayed()
        self.assertFalse(self.heading_earth.is_displayed())
        self.assertTrue(self.heading_world.is_displayed())

        # Toggle again and re-check
        self.button_toggle_heading.click()
        self.heading_earth.wait_until_is_displayed()
        self.assertTrue(self.heading_earth.is_displayed())
        self.assertFalse(self.heading_world.is_displayed())

    def test_login(self):
        from django.contrib.auth.hashers import make_password
        from django.contrib.auth.models import User

        browser_name = self.selenium.capabilities['browserName']
        browser_version = self.selenium.capabilities['version']
        if browser_name == 'phantomjs' and browser_version == '2.1.1':
            raise SkipTest("https://github.com/ariya/phantomjs/issues/14228")

        User.objects.create(username='alice',
                            password=make_password('topsecret'),
                            is_active=True)

        # Verify we aren't logged on
        self.selenium.get(self.live_server_url)
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'No user is logged on.')

        # Log on
        r = self.selenium.login(username='alice', password='topsecret')
        self.assertTrue(r)

        # Verify we are logged on
        self.selenium.get(self.live_server_url)
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'The logged on user is alice.')

        # Log out
        self.selenium.logout()

        # Verify we are logged out
        self.selenium.get(self.live_server_url)
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'No user is logged on.')

    def test_wait_until_n_windows(self):
        self.selenium.get(self.live_server_url)

        # Waiting for two windows should fail as there's only one
        with self.assertRaises(AssertionError):
            self.selenium.wait_until_n_windows(n=2, timeout=1)

        # Open a window and check again
        self.button_open_window.click()
        self.selenium.wait_until_n_windows(n=2, timeout=1)

        # Close the window
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        self.selenium.close()
        self.selenium.switch_to_window(self.selenium.window_handles[0])

    def test_exists(self):
        self.selenium.get(self.live_server_url)

        # Element with id=togglable does not exist. Check that the various
        # waits and asserts are ok.
        self.togglable.wait_until_not_exists()
        self.assertFalse(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_exists(timeout=1)

        # Create element with id=togglable...
        self.button_toggle_element.click()

        # ...and check things are opposite
        self.togglable.wait_until_exists()
        self.assertTrue(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_not_exists(timeout=1)

        # Destroy the element...
        self.button_toggle_element.click()

        # ...and check once more
        self.togglable.wait_until_not_exists()
        self.assertFalse(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_exists(timeout=1)

    def test_is_displayed(self):
        self.selenium.get(self.live_server_url)

        # Element with id=world is not displayed (but it exists). Check that
        # the various waits and asserts are ok.
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_not_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_is_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertFalse(self.heading_world.is_displayed())

        # Show the element
        self.button_toggle_heading.click()

        # ...and check things are opposite
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_is_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertTrue(self.heading_world.is_displayed())

        # Hide again...
        self.button_toggle_heading.click()

        # ...and check once more
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_not_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_is_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertFalse(self.heading_world.is_displayed())

    def test_contains(self):
        self.selenium.get(self.live_server_url)

        # Message does not contain 'world'. Check that the various waits
        # and asserts are OK.
        self.message.wait_until_contains('earth')
        self.message.wait_until_not_contains('world')
        with self.assertRaises(TimeoutException):
            self.message.wait_until_contains('world', timeout=1)
        with self.assertRaises(TimeoutException):
            self.message.wait_until_not_contains('earth', timeout=1)
        self.assertTrue('earth' in self.message.text)
        self.assertFalse('world' in self.message.text)

        # Toggle...
        self.button_toggle_message.click()

        # and check things are opposite
        self.message.wait_until_contains('world')
        self.message.wait_until_not_contains('earth')
        with self.assertRaises(TimeoutException):
            self.message.wait_until_contains('earth', timeout=1)
        with self.assertRaises(TimeoutException):
            self.message.wait_until_not_contains('world', timeout=1)
        self.assertTrue('world' in self.message.text)
        self.assertFalse('earth' in self.message.text)


@override_settings(SELENIUM_WEBDRIVERS=False)
class DjangoSeleniumCleanSkipTestCase(TestCase):

    def test_skip_test(self):
        # Create and instantiate a dummy SeleniumTestCase
        class SkippedTestCase(SeleniumTestCase):
            def runTest(self):
                pass
        instance = SkippedTestCase()

        # OK, now let's "execute" the dummy test case. Any attempt to access
        # the self.selenium shall result in an error, since
        # upon such access self.selenium will try to initialize itself, which
        # will not be possible since we have overridden the SELENIUM_WEBDRIVERS
        # setting to be empty. But SkippedTestCase does not access
        # self.selenium (in our case because it's dummy; in a real
        # use case because the Selenium test might be skipped). Therefore the
        # "executing" of the test case should raise no error.
        instance()


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()
management.call_command('migrate')
