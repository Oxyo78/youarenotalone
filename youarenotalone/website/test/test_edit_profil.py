from time import sleep
from django.test import TestCase
from website.models import Interest, UserProfile, City, News
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import Select

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

    def test_edit_profile(self):
        """ Add an interest to the user """
        timeout = 2
        # Log with a user
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('login-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('connect').click()
        # Try short password
        self.selenium.find_element_by_id('account-nav').click()
        self.selenium.find_element_by_id('editButton').click()
        newPassword = self.selenium.find_element_by_id("passwordInput")
        newPassword.send_keys('Paul')
        newPassword2 = self.selenium.find_element_by_id("password2Input")
        newPassword2.send_keys('Paul')
        self.selenium.find_element_by_id('saveButton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert_message = self.selenium.find_element_by_id("errorText").text
        self.assertEqual(alert_message, "Le mot de passe est trop semblable au champ « nom d'utilisateur ». Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères. Ce mot de passe est trop courant.")