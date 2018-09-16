from django.test import TestCase
from django.test import Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.auth.models import User
from .models import Interest, UserProfile, City, News

class UrlTestCase(TestCase):
    """ URL test """
    fixtures = ['city.json', 'interest.json', 'user.json', 'userprofile.json', 'message.json']

    def setUp(self):
        self.client = Client()

    def test_url(self):
        # Anonymous user
        home = self.client.get('')
        logout = self.client.get('/logout/')
        legal = self.client.get('/legal/')
        messageOff = self.client.get('/messages/')
        messageViewOff = self.client.get('/messages/view/2/#messageTag')
        accountOff = self.client.get('/account/')

        # logged in user
        self.client.login(username='Paul', password='azerty')
        message = self.client.get('/messages/')
        messageView = self.client.get('/messages/view/2/#messageTag')
        account = self.client.get('/account/')
        
        self.assertEqual(home.status_code, 200)
        self.assertEqual(logout.status_code, 302)
        self.assertEqual(legal.status_code, 200)
        self.assertEqual(messageOff.status_code, 302)
        self.assertEqual(message.status_code, 200)
        self.assertEqual(messageViewOff.status_code, 302)
        self.assertEqual(messageView.status_code, 200)
        self.assertEqual(accountOff.status_code, 302)
        self.assertEqual(account.status_code, 200)

    def test_search(self):
        """Test the search function and the json return in AJAX """
        self.client.login(username='Paul', password='azerty')
        result = self.client.get('/search/', { 'searchInterest': 1 }, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(result.json(), {'Yohan': {'Lat': '5.9580075924', 'Lng': '45.4615911720', 'name': 'Yohan'}})
    


class FirstSeleniumTests(StaticLiveServerTestCase):
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
        self.selenium.find_element_by_id('login').click()
        username_input = self.selenium.find_element_by_id("usernameInputControl")
        username_input.send_keys('Paul')
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
        selectInput = self.selenium.find_element_by_id("citySelect")
        for option in selectInput.find_elements_by_tag_name('AAST'):
            if option.text == 'AAST':
                option.click() # select() in earlier versions of webdriver
                break
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