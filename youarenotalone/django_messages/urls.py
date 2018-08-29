from django.urls import path
from django.views.generic import RedirectView
from . import views
from django_messages.views import *

urlpatterns = [
    path('compose/', compose, name='messages_compose'),
    path('compose/<recipient>/', compose, name='messages_compose_to'),
    path('reply/<message_id>/', reply, name='messages_reply'),
    path('delete/<message_id>/', delete, name='messages_delete'),
]
