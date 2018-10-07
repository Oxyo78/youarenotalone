from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django_messages.views import delete

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('messages/', views.messageInbox, name='message'),
    path('messages/view/<messageId>/', views.viewMessage, name='view_message'),  
    path('account/', views.account, name='account'),
    path('search/', views.searchUsers, name='search'),
    path('newMessage/', views.newMessage, name='newMessage'),
    path('legal/', views.legalize, name='legalize'),
    path('complete-city/', views.completeCity, name='cityComplete'),
    path('account/complete-city/', views.completeCity, name='cityComplete'),
    path('acceptCookies/', views.acceptCookies, name='acceptCookie'),
]