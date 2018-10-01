from django.test import TestCase
from website.models import Interest, UserProfile, City, News
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from django.contrib.staticfiles.testing import StaticLiveServerTestCase



class UserSeleniumTests(StaticLiveServerTestCase):
    """ Try connexion and logout of a user """
    fixtures = ['city.json', 'interest.json', 'user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        """ Login & disconnect user """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('login-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azerty')
        self.selenium.find_element_by_id('connect').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('account-nav'))
        self.selenium.find_element_by_id('logout-nav').click()

    def test_create_user(self):
        """ Create user """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul02')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul2@example.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('AAST')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azertyu7')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azertyu7')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('account-nav'))
        self.selenium.find_element_by_id('logout-nav').click()

        """ Login with the new account """
        self.selenium.find_element_by_id('login-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul02')
        password_input = self.selenium.find_element_by_id("passwordControl")
        password_input.send_keys('azertyu7')
        self.selenium.find_element_by_id('connect').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('account-nav'))
        self.selenium.find_element_by_id('logout-nav').click()

    def test_name_already_taken(self):
        """ Test username already taken """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul@example.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('AAST')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azertyu7')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azertyu7')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert = self.selenium.find_element_by_id("errorAlert")
        alert_message = alert.find_element_by_xpath("//strong").text
        self.assertCountEqual(alert_message, "Nom d'utilisateur déja pris")

    def test_city_name_not_found(self):
        """ Test city name not found """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul03')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul@example.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('wrongCityName')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azertyu7')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azertyu7')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert = self.selenium.find_element_by_id("errorAlert")
        alert_message = alert.find_element_by_xpath("//strong").text
        self.assertCountEqual(alert_message, "Le nom de ville entrée n'a pas été trouvé")

    def test_wrong_email_input(self):
        """ Test email input from user """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul03')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paulexample.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('AAST')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azertyu7')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azertyu7')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert = self.selenium.find_element_by_id("errorAlert")
        alert_message = alert.find_element_by_xpath("//strong").text
        self.assertCountEqual(alert_message, "L'email n'est pas valide")
    
    def test_password_contain_one_number(self):
        """ Test password without number """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul03')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul@example.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('AAST')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('azertyui')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('azertyui')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert = self.selenium.find_element_by_id("errorAlert")
        alert_message = alert.find_element_by_xpath("//strong").text
        self.assertCountEqual(alert_message, "Le mot de passe doit contenir au moins 1 chiffre")

    def test_password_contain_only_number(self):
        """ Test password with only number """
        timeout = 2
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('signin-nav').click()
        username_input = self.selenium.find_element_by_id("usernameInput")
        username_input.send_keys('Paul03')
        password_input = self.selenium.find_element_by_id("emailInput")
        password_input.send_keys('paul@example.com')
        city_input = self.selenium.find_element_by_id("cityInput")
        city_input.send_keys('AAST')
        password_input = self.selenium.find_element_by_id("passwordInput")
        password_input.send_keys('12345678')
        password_input = self.selenium.find_element_by_id("password2Input")
        password_input.send_keys('12345678')
        self.selenium.find_element_by_id('subscribebutton').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('alertMessage'))
        alert = self.selenium.find_element_by_id("errorAlert")
        alert_message = alert.find_element_by_xpath("//strong").text
        self.assertCountEqual(alert_message, "Le mot de passe doit contenir au moins 1 lettre")
