from time import sleep
from django.test import TestCase
from website.models import Interest, UserProfile, City, News
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class NavigationOffSeleniumTests(StaticLiveServerTestCase):
    """ Try the navigation of a anonymous user """
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

    def test_cookie_modal(self):
        """ Test the cookies popup """
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        a = WebDriverWait(self.selenium, 6).until(
            EC.element_to_be_clickable((By.ID, 'cookiesButton')))
        self.selenium.find_element_by_id('cookiesButton').click()

    def test_news_link(self):
        """ Home page link """
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('news-nav').click()
        self.selenium.find_element_by_id("services")

    def test_youarenotalone_link(self):
        """ Test the title link back home """
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('titlePage').click()
        element = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "slideword"))
            )

    def test_legalize_link(self):
        """ Test the "Mention légales" link """
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('legalizeLink').click()
        element = WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, "legalize"))
            )
    
    def test_contact_link(self):
        """ Test the contact link """
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        self.selenium.find_element_by_id('contactLink')
