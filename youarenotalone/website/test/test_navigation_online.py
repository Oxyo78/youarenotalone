from time import sleep
from django.test import TestCase
from website.models import Interest, UserProfile, City, News
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NavigationOnSeleniumTests(StaticLiveServerTestCase):
    """ Try the navigation of a logged user """
    fixtures = ['city.json', 'interest.json', 'user.json', 'message.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_logged_user_link(self):
        """Test all url for logged user """
        # Log with a user
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('login-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('connect').click()
        WebDriverWait(self.selenium, 3).until(
            lambda driver: driver.find_element_by_id('account-nav'))
        # Accept the cookies condition
        WebDriverWait(self.selenium, 6).until(
            lambda driver: driver.find_element_by_id("cookiesModal"))
        sleep(3)
        self.selenium.find_element_by_id('cookiesButton').click()
        # Click on the account link
        sleep(2)
        self.selenium.find_element_by_id('account-nav').click()
        # Click on message link
        self.selenium.find_element_by_id('message-nav').click()
        # Open a message view
        self.selenium.find_element_by_partial_link_text('RE:').click()
        # Answer to the message
        body = self.selenium.find_element_by_id('bodyReply')
        body.send_keys('Hello boy !')
        self.selenium.find_element_by_id('sendButton').click()
        WebDriverWait(self.selenium, 3).until(
            lambda driver: driver.find_element_by_id("succesAlert"))
        alertMessage = self.selenium.find_element_by_css_selector('strong.text').text
        self.assertAlmostEqual(alertMessage, 'Message envoyé')