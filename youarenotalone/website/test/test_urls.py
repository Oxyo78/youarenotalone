from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from website.models import Interest, UserProfile, City, News
from django_messages.models import Message, inbox_count_for

class UrlTestCase(TestCase):
    """ URL test """
    fixtures = ['city.json', 'interest.json', 'user.json', 'userprofile.json', 'message.json']

    def setUp(self):
        self.client = Client()

    def test_url(self):
        # Anonymous user
        home = self.client.get('')
        logoutOff = self.client.get('/logout/')
        legal = self.client.get('/legal/')
        messageOff = self.client.get('/messages/')
        messageViewOff = self.client.get('/messages/view/2/#messageTag')
        accountOff = self.client.get('/account/')

        # logged in user
        self.client.login(username='Paul', password='azerty')
        message = self.client.get('/messages/')
        messageView = self.client.get('/messages/view/2/#messageTag')
        account = self.client.get('/account/')
        logout = self.client.get('/logout/')
        
        self.assertEqual(home.status_code, 200)
        self.assertEqual(logoutOff.status_code, 302)
        self.assertEqual(logout.status_code, 302)
        self.assertEqual(legal.status_code, 200)
        self.assertEqual(messageOff.status_code, 302)
        self.assertEqual(message.status_code, 200)
        self.assertEqual(messageViewOff.status_code, 302)
        self.assertEqual(messageView.status_code, 200)
        self.assertEqual(accountOff.status_code, 302)
        self.assertEqual(account.status_code, 200)

    def test_search(self):
        """ Test the search function and the json return in AJAX """
        self.client.login(username='Paul', password='azerty')
        result = self.client.get('/search/', { 'searchInterest': 1 }, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(result.json(), {'Yohan': {'Lat': '5.9580075924', 'Lng': '45.4615911720', 'name': 'Yohan'}})

    def test_completeCity(self):
        """ Test the autocomplete city in Ajax """
        result = self.client.get('/complete-city/', { 'term': "aas" }, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(result.json(), ['AAST 12345'])

    def test_new_message(self):
        self.client.login(username='Paul', password='azerty')
        result = self.client.post('/newMessage/', 
                {'body': 'This is a test message recipient', 'subject': 'subject test', 'recipient': 'Yohan' },
                 HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
        self.assertEqual(result.json(), {'loginSuccess': 'True', 'succesText': 'Message envoyé'})
    
    def test_view_message(self):
        self.client.login(username='Paul', password='azerty')
        message = self.client.get('/messages/')
        print(message.content)


    def test_message_inbox(self):
        pass

    def test_account_form(self):
        pass