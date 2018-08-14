from django.test import TestCase
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class UrlTestCase(TestCase):
    """ URL test """

    def setUp(self):
        self.client = Client()

    def test_url(self):
        home = self.client.get('')
        logout = self.client.get('logout/')

        self.assertEqual(home.status_code, 200)
        self.assertEqual(logout.status_code, 404)


class MySeleniumTests(StaticLiveServerTestCase):
    """ Try connexion and logout of a user """
    fixtures = ['user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        """ Login & disconnect user """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('login').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul01')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('connect').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('account'))
        self.selenium.find_element_by_id('logout').click()

    def test_create_user(self):
        """ Create user """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul02')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul@example.com')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azerty')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('subscribebutton').click()
        self.selenium.find_element_by_id('logout').click()

        """ Login with the new account """
        self.selenium.find_element_by_id('login').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul02')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('connect').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('account'))
        self.selenium.find_element_by_id('logout').click()
