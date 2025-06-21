from django.urls import path
from .views import homepage, about, contact, subscribe_newsletter


urlpatterns = [
    path('', homepage, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
]